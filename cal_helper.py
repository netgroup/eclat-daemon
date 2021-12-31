"""
Command Abstraction Layer helper

This module simplifies the access to the Command Abstraction Layer

"""
import subprocess
import os
import json
import cal
import ipaddress

#cal.bpftool_map_update(pm.map_path, ["01","00","00", "00"], ["01", "00", "00", "00","00", "00","00", "00"], map_reference_type="pinned", value_type="hex")

def cal_map_update(map_reference, key, value, key_bytes=4, value_bytes=8):
    key_list = []
    for i in range (0,key_bytes):
        key_list.append("{:02x}".format(key % 256))
        key = key >> 8
    value_list = []
    for i in range (0,value_bytes):
        value_list.append("{:02x}".format(value % 256))
        value = value >> 8
    #print (key_list)
    #print (value_list)

    cal.bpftool_map_update(pm.map_path, key_list, value_list, map_reference_type="pinned", value_type="hex")    


cal_map_update("pluto", 256, 2**32-1, key_bytes=4, value_bytes=8)


