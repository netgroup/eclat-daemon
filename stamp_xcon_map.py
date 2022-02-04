import os
import json
import subprocess
from time import sleep

# Command Abstraction Layer
import cal
import hex_types as ht

OUT_INTF_INDEX = 5
IN_INTF_INDEX = 4

BASE_PATH =  '/sys/fs/bpf/maps'
PACKAGE = 'mynet'
PROGRAM = 'l2xcon'
MAP = 'l2xcon_map'
map_path = f"{BASE_PATH}/{PACKAGE}/{PROGRAM}/{MAP}"
map_as_array = []

if not os.path.exists(map_path):
      print(f"path to {map_path} does not exist")
else:
      try :
            cal.cal_map_update(map_path, ht.u32(IN_INTF_INDEX), ht.u32(OUT_INTF_INDEX))
            map_as_array = json.loads(cal.bpftool_map_dump(map_path))
            print(f"updated map:\n{map_as_array}")
      except Exception as e:
            print(e)
            print(map_path)
