"""
Parse the json obtained as the output of the compiling process.

The output of the parser is list of dict for map information and a dict for program information

The primitive types are:
('uint', n) n is the number of bits
('sint', n) n is the number of bits
('byte_array', n) n is the number of bytes

example of program information
hike_program_info = {'param_num': 2, 'param_types': [('int', 32), ('int', 64)]}

example 1 of map information (with only one map)
map_info_list = [{'map_name': 'ipv6_simple_classifier_map', 'key_type': ('int', 32), 'value_type': ('int', 32)}]

the key is:
('int', 32)

the value is:
('int', 32)

example 2 of map information (with only one map)
[{'map_name': 'ipv6_hset_srcdst_map', 'key_type': [[('byte_array', 16)], [('byte_array', 16)]], 'value_type': [('int', 64), ('int', 64)]}]

the key is:
[[('byte_array', 16)], [('byte_array', 16)]]

the value is:
[('int', 64), ('int', 64)]

There are two primitive types, represented as
('int', n) 
n is the number of bits

('byte_array', n)
n is the number of bytes

The byte arrays are currently used when there are union types

TODO (?)
provide additional metadata like for example the name of fields of the structures

in case of the UNIONS, represent the different options

https://replit.com/@StefanoSalsano/HIKEeProgInfoParser
"""


import json


def parse_info(input_file):
    """Parse the JSON file produced by the compiling process.

    :param input_file: json file (path)
    :return: (maps_info, hike_program_info)
    :rtype: maps_info is a list of dict, one for each map, hike_program_info is a dict
    """
    data = {}
    maps_info = []
    hike_program_info = {}

    def get_by_id(type_id):
        for type in data['types']:
            if type['id'] == type_id:
                if type['kind'] == 'VAR':
                    return get_by_id(type['type_id'])
                elif type['kind'] == 'PTR':
                    return get_by_id(type['type_id'])
                else:
                    return type

    def get_type(type_id):
        my_dict = get_by_id(type_id)
        if my_dict['kind'] == 'STRUCT':
            my_struct = []
            for member in my_dict['members']:
                my_struct.append(get_type(member['type_id']))
            return my_struct
        if my_dict['kind'] == 'ARRAY':
            my_arr = []
            for counter in range(my_dict['nr_elems']):
                my_arr.append(get_type(my_dict['type_id']))
            return my_arr
        if my_dict['kind'] == 'TYPEDEF':
            return get_type(my_dict['type_id'])
        if my_dict['kind'] == 'UNION':
            return ('byte_array', my_dict['size'])
        if my_dict['kind'] == 'INT':
            if my_dict['nr_bits'] != my_dict['size']*8:
                print('ERROR in INT: nr_bits != size * 8')
                exit(-1)
            if (my_dict['encoding']) == '(none)':
                return ('uint', my_dict['nr_bits'])
            elif (my_dict['encoding']) == 'SIGNED':
                return ('sint', my_dict['nr_bits'])
            else:
                print('ERROR in INT: unknown encoding')
                exit(-1)

        print('unmatched kind:', my_dict['kind'], type_id)

    # with open(INPUT_FILE) as f:
    with open(input_file) as f:
        data = json.load(f)
        for type in data['types']:
            if type['kind'] == 'DATASEC' and type['name'] == '.hike.maps.export':
                for v in type['vars']:
                    my_map = {}
                    map_type = get_by_id(v['type_id'])
                    map_name = map_type['members'][1]['name']
                    my_map['map_name'] = map_name
                    type_id = map_type['members'][1]['type_id']
                    map_types = get_by_id(type_id)
                    key_type_id = map_types['members'][0]['type_id']
                    value_type_id = map_types['members'][1]['type_id']
                    #print (get_by_id(key_type_id))
                    #print (get_by_id(value_type_id))
                    types_for_key = get_type(key_type_id)
                    # print(types_for_key)
                    # if type(types_for_key) is list:
                    if isinstance(types_for_key, list):
                        my_map['key_type'] = types_for_key
                    else:
                        my_map['key_type'] = [types_for_key]
                    types_for_value = get_type(value_type_id)
                    # print(types_for_value)
                    if isinstance(types_for_value, list):
                        my_map['value_type'] = types_for_value
                    else:
                        my_map['value_type'] = [types_for_value]
                    maps_info.append(my_map)
            if type['kind'] == 'DATASEC' and type['name'] == '.hike.prog.export':
                for v in type['vars']:
                    prog_type = get_by_id(v['type_id'])
                    # print(prog_type['params'])
                    hike_program_info['param_num'] = len(prog_type['params'])
                    my_params = []
                    for p in prog_type['params']:
                        my_params.append(get_type(p['type_id']))
                    hike_program_info['param_types'] = my_params
        return (maps_info, hike_program_info)


def flatten(l):
    """Flatten a list of lists

    :param l: nested list
    :type l: list
    :return: flatten list
    :rtype: list
    """
    out = []
    for item in l:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out


def get_type_fmt(datatypes):
    """
    Returns the format according to python struct.pack of the datatypes.
    Datatypes are a flatten list of types e.g. (type, size)
    where type can be sint, uint or byte_array, and size is expressed in bits for the formers and byte for the last one
    """
    fmt = "<"
    for k in datatypes:
        type, size = k
        if type == 'uint':
            if size == 16:
                fmt += "H"
            elif size == 32:
                fmt += "I"
            elif size == 64:
                fmt += "Q"
        elif type == 'sint':
            if size == 16:
                fmt += "h"
            elif size == 32:
                fmt += "i"
            elif size == 64:
                fmt += "q"
        elif type == 'byte_array':
            fmt += f"{size}c"
    return fmt
