import json

k_size, v_size = None, None
with open("../hike_v3/src/.output/ip6_simple_classifier.bpf.json") as f:
    data = json.load(f)
    for type in data['types']:
        if type['kind'] == 'STRUCT' and type['name'].startswith('____btf_map_ipv6_simple_classifier_map'):
            k, v = type['members']
            k_type = data['types'][k['type_id']]
            v_type = data['types'][v['type_id']]
            assert(k_type['kind'] == 'INT')
            assert(v_type['kind'] == 'INT')
            k_size = k_type['size']
            v_size = v_type['size']
            print(k_type)
            print(v_type)

chain_bytes = (86).to_bytes(v_size, byteorder='little')
print(" ".join([f"{c:02x}" for c in chain_bytes]))
