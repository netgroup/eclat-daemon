import os
import json
import subprocess

# Command Abstraction Layer
import cal
import hex_types as ht

BASE_PATH =  '/sys/fs/bpf/maps'
PACKAGE = 'misc'
PROGRAM = 'time'
MAP = 'map_time'
map_path = f"{BASE_PATH}/{PACKAGE}/{PROGRAM}/{MAP}"
map_as_array = []

if os.path.exists(map_path):
  try :
        map_as_array = json.loads(cal.bpftool_map_dump(map_path))
  except Exception as e:
        print (e)
        print (map_path)
else:
    print("path does not exist")

# map_as_array contains the map as a list of (key, value) pairs
print (map_as_array)

ret = subprocess.run("./t2", capture_output=True)
delta = int(ret.stdout)
print(f"delta: {delta}")
cal.cal_map_update(map_path, ht.u32(2**32-1), delta)
# cal.bpftool_map_update(map_path, ["00", "00", "00", "00"], to_hex(delta), value_type="hex")