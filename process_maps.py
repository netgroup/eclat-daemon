import json
import os
import subprocess
import ipaddress
import cal
import hex_types as ht

BASE_PATH =  '/sys/fs/bpf/maps'
EXCLUDE_ADDRS = "fe80::", "ff02::"

def out_ip6_sd(src_ip6, dst_ip6):
    return f"{src_ip6}".ljust(25)+"- "+f"{dst_ip6}".ljust(25)

def out_ns(value):
    intero = int(value/1000000000)
    vstring=str(value)

    return f"{intero}.{vstring[len(str(intero)):]}"

def get_ip6_sd_from_key(key):
    if 'saddr' in key:
        src_ip6 = ipaddress.IPv6Address(ht.ipv6_int128_from_int8(key['saddr']['in6_u']['u6_addr8']))
    else:
        src_ip6 = '*'
    if 'daddr' in key:
        dst_ip6 = ipaddress.IPv6Address(ht.ipv6_int128_from_int8(key['daddr']['in6_u']['u6_addr8']))
    else:
        src_ip6 = '*'
    return (src_ip6,dst_ip6)

def process_pcpu_values_u64(val_array):
    num_val_array = []
    str_details = ""
    for val in val_array:
        num_val_array.append(val['value'])
        str_details=str_details+str(val['value']).rjust(7)+':'
    return (num_val_array, str_details)

def process_pcpu_values_struct_count(val_array):
    num_val_array = []
    str_details = ""
    for val in val_array:
        num_val_array.append(val['value']['count'])
        str_details=str_details+str(val['value']['count']).rjust(7)+':'
    return (num_val_array, str_details)


class ProcessMap:

    def __init__(self, map_name, package='system', program=None):

        self.package = package
        self.program = program
        self.map_name = map_name

        if package == 'system' :
            self.map_path = f"{BASE_PATH}/system/{self.map_name}"
        else:     
            self.map_path = f"{BASE_PATH}/{self.package}/{self.program}/{self.map_name}" 

    def read(self):
         
        self.map_as_array = []
        
        if os.path.exists(self.map_path):
            try :
                self.map_as_array = json.loads(cal.bpftool_map_dump(self.map_path))

            except Exception as e:
                print (e)
                print (self.map_path)
                return -1
        else:
            return -1
        return 0

if __name__ == "__main__":

    pm = ProcessMap('pcpu_sd_tbmon','meter','ip6_sd_tbmon')
    
    result = pm.read()
    if result == 0 :
        #print (json.dumps(pm.map_as_array))
        output_rows = []
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            for v in my_obj['values']:
                if v['value']['last_time'] != 0:
                    output_rows.append (out_ip6_sd(src_ip6, dst_ip6) + 
                        f" cpu: {v['cpu']} time: {out_ns(v['value']['last_time'])} "+
                        f"tokens: "+f"{v['value']['last_tokens']}".rjust(8))
        output_rows.sort()
        output_rows = filter(lambda line : not any([el in line for el in EXCLUDE_ADDRS]), output_rows)
        for element in output_rows:
            print (element)

        #experiment to add an entry to the map    
        #ipa = ipaddress.IPv6Address('::74')
        #ipb = ipaddress.IPv6Address('cafe::')
        #v = [ht.u64(100),ht.u64(100),ht.u64(1000),ht.u64(1000),ht.u64(100),ht.u64(100)]
        #cal.cal_map_update(pm.map_path, [ipa,ipb], v)

    pm = ProcessMap('map_pcpu_lse','hike_default','lse')
    
    result = pm.read()
    if result == 0 :
        #print (pm.map_as_array)
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            for v in my_obj['values']:
                print (out_ip6_sd(src_ip6, dst_ip6) + 
                    f" cts: {out_ns(v['value']['cts_ns'])} timeout: {out_ns(v['value']['timeout_ns'])}")

                    
    pm = ProcessMap('ipv6_hset_sd_map','hike_default','ip6_hset_srcdst')
    result = pm.read()
    if result == 0 :
        for my_obj in pm.map_as_array :
            #print (my_obj)
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            print (out_ip6_sd(src_ip6, dst_ip6) + 
                f" cts: {out_ns(my_obj['value']['cts_ns'])} timeout: {out_ns(my_obj['value']['timeout_ns'])}")


    pm = ProcessMap('map_pcpu_mon','hike_default','monitor')
    result = pm.read()
    if result == 0 :
        for my_obj in pm.map_as_array :

            (num_val_array,str_details) = process_pcpu_values_u64(my_obj['values'])

            print (f"{my_obj['key']}".rjust(3)+" : "+f"{sum(num_val_array)}".rjust(8)+" "+str_details)
    
        #experiment to update a key value pair
        #print (pm.map_path)
        #cal.bpftool_map_update(pm.map_path, ["01","00","00", "00"], ["01", "00", "00", "00","00", "00","00", "00"], map_reference_type="pinned", value_type="hex")
        #cal.cal_map_update(pm.map_path, ht.u32(256), 256)


    pm = ProcessMap('pcpu_meter','meter','ip6_sd_meter')
    result = pm.read()
    if result == 0 :
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            (num_val_array,str_details) = process_pcpu_values_struct_count(my_obj['values'])
            print (out_ip6_sd(src_ip6, dst_ip6)+f"{sum(num_val_array)}".rjust(8)+str_details)

    pm = ProcessMap('pcpu_dst_meter','meter','ip6_dst_meter')
    result = pm.read()
    if result == 0 :
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            (num_val_array,str_details) = process_pcpu_values_struct_count(my_obj['values'])
            print (out_ip6_sd(src_ip6, dst_ip6)+f"{sum(num_val_array)}".rjust(8)+str_details)


    pm = ProcessMap('pcpu_tb_dst','meter','ip6_dst_tbmon')
    result = pm.read()
    if result == 0 :
        output_rows = []
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            for v in my_obj['values']:
                if v['value']['last_time'] != 0:
                    output_rows.append (out_ip6_sd(src_ip6, dst_ip6) + 
                        f" cpu: {v['cpu']} time: {out_ns(v['value']['last_time'])} "+
                        f"tokens: "+f"{v['value']['last_tokens']}".rjust(8))
        output_rows.sort()
        output_rows = filter(lambda line : not any([el in line for el in EXCLUDE_ADDRS]), output_rows)
        for element in output_rows:
            print (element)

    pm = ProcessMap('pcpu_sd_dec2zero','sampler','ip6_sd_dec2zero')
    result = pm.read()
    if result == 0 :
        for my_obj in pm.map_as_array :
            (src_ip6,dst_ip6) = get_ip6_sd_from_key(my_obj['key'])
            (num_val_array,str_details) = process_pcpu_values_struct_count(my_obj['values'])
            print (out_ip6_sd(src_ip6, dst_ip6)+f"{sum(num_val_array)}".rjust(8)+str_details)