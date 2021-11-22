import json
import os
import subprocess
import ipaddress

BASE_PATH =  '/sys/fs/bpf/maps'

def ipv6_int128_from_int8(input_list):
    ipv6_int128 = 0
    i = 15
    for int8 in input_list:
        ipv6_int128 = ipv6_int128 | (int8 << (i*8))
        i = i - 1
    #print (ipv6_int128)
    return ipv6_int128

def out_ns(value):
    intero = int(value/1000000000)
    vstring=str(value)

    return f"{intero}.{vstring[len(str(intero)):]}"

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
        #map_path = f"{BASE_PATH}/{self.package}/{self.program}/{self.map_name}"
        if os.path.exists(self.map_path):
            my_command = f"bpftool map dump pinned {self.map_path}".split()
            result = subprocess.run(my_command, stdout=subprocess.PIPE)
            if self.package == 'system':
                print(result.stdout.decode('utf-8'))
            self.map_as_array = json.loads(result.stdout.decode('utf-8'))
            return 0
        else:
            print ("Error: map_path does not exists")
            print (self.map_path)

        return -1
        

if __name__ == "__main__":

    if True:
        pm = ProcessMap('pcpu_sd_tbmon','mynet','ip6_sd_tbmon')
        
        result = pm.read()
        if result != 0 :
            exit(-1)
        #print (pm.map_as_array)
        for my_obj in pm.map_as_array :
            #print (my_obj['key']['saddr']['in6_u']['u6_addr8'],my_obj['key']['daddr']['in6_u']['u6_addr8'])
            src_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['saddr']['in6_u']['u6_addr8']))
            if src_ip6 == ipaddress.IPv6Address('fc01::1'):  
                dst_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['daddr']['in6_u']['u6_addr8']))
                if dst_ip6 == ipaddress.IPv6Address('fc01::2'):
                    for v in my_obj['values']:
                        if v['value']['last_time'] != 0:
                            print (f"cpu: {v['cpu']} time: {out_ns(v['value']['last_time'])}")

    if False:    
        pm3 = ProcessMap('map_pcpu_lse','net','lse')
        
        result = pm3.read()
        if result != 0 :
            exit(-1)
        #print (pm.map_as_array)
        for my_obj in pm3.map_as_array :
            #print (my_obj)
            #break
            #print (my_obj['key']['saddr']['in6_u']['u6_addr8'],my_obj['key']['daddr']['in6_u']['u6_addr8'])
            src_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['saddr']['in6_u']['u6_addr8']))
            if src_ip6 == ipaddress.IPv6Address('fc01::1'):  
                dst_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['daddr']['in6_u']['u6_addr8']))
                if dst_ip6 == ipaddress.IPv6Address('fc01::2'):
                    for v in my_obj['values']:
                        print (f"cts: {out_ns(v['value']['cts_ns'])} timeout: {out_ns(v['value']['timeout_ns'])}")


                    
    pm2 = ProcessMap('ipv6_hset_sd_map','mynet','ip6_hset_srcdst')
    #pm2 = ProcessMap('ipv6_hset_srcdst_map','net','ip6_hset_srcdst')
    result = pm2.read()
    if result != 0 :
        exit(-1)
    for my_obj in pm2.map_as_array :
        #print (my_obj)
        src_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['saddr']['in6_u']['u6_addr8']))
        dst_ip6 = ipaddress.IPv6Address(ipv6_int128_from_int8(my_obj['key']['daddr']['in6_u']['u6_addr8']))
        print (src_ip6, dst_ip6,f"cts: {out_ns(my_obj['value']['cts_ns'])} timeout: {out_ns(my_obj['value']['timeout_ns'])}")

