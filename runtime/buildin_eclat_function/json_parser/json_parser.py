import json


def bpf_map(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    json_dict = {}
    for types in data["types"]:
        json_dict[types["id"]] = types

    json_output = []
    for obj in json_dict:
        if json_dict[obj]["kind"] == "DATASEC" \
                and json_dict[obj]["name"] == ".hike.maps.export":
            for var in json_dict[obj]["vars"]:
                hike_map_export = json_dict[var["type_id"]]
                
                ###### STRUTTURA: PROGRAMMA - MAPPA #####
                struct = json_dict[hike_map_export["type_id"]]
                #print("\nPROGRAMMA - MAPPA \n", struct)
                ##############################

                json_output.append({
                    "program": {
                        "name": struct["members"][0]["name"],
                        "members": read_members(struct["members"][0], json_dict)
                    },
                    "map": {
                        "name": struct["members"][1]["name"],
                        "members":read_members(struct["members"][1], json_dict)
                    }
                })

    return json_output


def read_members(json_obj, json_dict):
    # Se non contiene le chiavi "members" e "type_id" allora
    # può essere un tipo semplice (else) oppure una funzione (FUNC_PROTO)
    if not "members" in json_obj and not "type_id" in json_obj:
        if json_obj["kind"] == "FUNC_PROTO":
            params = []
            for param in json_obj["params"]:
                #print("\nPARAM\n", param, type(param), type(json_obj))
                params.append(read_members(json_dict[param["type_id"]], json_dict))
            return {
                'kind': json_obj["kind"],
                'name': json_obj["name"],
                'return': read_members(json_dict[json_obj["ret_type_id"]], json_dict),
                'params': params
            }
        else:
            return {
                'kind': json_obj["kind"],
                'name': json_obj["name"],
                'size': json_obj["size"]
            }
    elif "members" in json_obj:
        members = []
        for member in json_obj["members"]:
            # Se è una struttura
            if json_dict[member["type_id"]]["kind"] == "STRUCT":
                members.append({
                    "name" : member["name"],
                    "type" : {
                        "kind": json_dict[member["type_id"]]["kind"],
                        "vars": read_members(member, json_dict)
                    }
                })
            # Se è un tipo semplice
            else:
                members.append({
                    "name": member["name"],
                    "type": read_members(member, json_dict)
                })
        return members

    elif "type_id" in json_obj:
        return read_members(json_dict[json_obj["type_id"]], json_dict)


# Pretty Printing JSON string back
output_file = open("output_json_parser.json", "w")

print(json.dumps(bpf_map("dump.json"), indent=4, sort_keys=True), file=output_file)

output_file.close()
