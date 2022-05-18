import os
import json
import argparse
from re import TEMPLATE
import subprocess
from time import sleep

# Command Abstraction Layer
import cal
import hex_types as ht

BASE_PATH =  '/sys/fs/bpf/maps'
PACKAGE = 'eip'
PROGRAM = 'mcd'
MAP = 'eip_mcd_time'
TEMPLATE = 16
ID = 0
LOAD = 0
map_as_array = []

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkg", metavar="pkg", default=PACKAGE, help="package name")
    parser.add_argument("--prog", metavar="prog", default=PROGRAM, help="program name")
    parser.add_argument("--map", metavar="map", default=MAP, help="map name")
    parser.add_argument("--template", metavar="template", type=int, default=TEMPLATE, help="tts template")
    parser.add_argument("--id", metavar="id", type=int, default=ID, help="interface ID")
    parser.add_argument("--load", metavar="load", type=int, default=LOAD, help="interface load")
    return parser.parse_args()

args = parse()
map_path = f"{BASE_PATH}/{args.pkg}/{args.prog}/{args.map}"
if not os.path.exists(map_path):
      print(f"path to {map_path} does not exist")
else:
      try :
            template = args.template
            id = args.id
            load = args.load
            print(f"template: {template}")
            cal.cal_map_update(map_path, ht.u8(1), template)
            print(f"ID: {id}")
            cal.cal_map_update(map_path, ht.u8(2), id)
            print(f"load: {load}")
            cal.cal_map_update(map_path, ht.u8(3), load)
            map_as_array = json.loads(cal.bpftool_map_dump(map_path))
            print(f"updated map:\n{map_as_array}")
      except Exception as e:
            print(e)
            print(map_path)
