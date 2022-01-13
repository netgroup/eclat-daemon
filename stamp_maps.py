import os
import json
import subprocess
from time import sleep

# Command Abstraction Layer
import cal
import hex_types as ht

BASE_PATH =  '/sys/fs/bpf/maps'
PACKAGE = 'stamp'
PROGRAM = 'stamp'
MAP = 'map_time'
TIME_EXEC = "develop/t2"
map_path = f"{BASE_PATH}/{PACKAGE}/{PROGRAM}/{MAP}"
map_as_array = []

if not os.path.exists(map_path):
      print(f"path to {map_path} does not exist")
elif not os.path.exists(TIME_EXEC):
      print(f"path to {TIME_EXEC} does not exist")
else:
      try :
            while(True):
                  ret = subprocess.run(TIME_EXEC, capture_output=True)
                  delta = int(ret.stdout)
                  print(f"delta: {delta}")
                  cal.cal_map_update(map_path, ht.u8(0), delta)
                  map_as_array = json.loads(cal.bpftool_map_dump(map_path))
                  print(f"updated map:\n{map_as_array}")
                  sleep(30)
      except Exception as e:
            print(e)
            print(map_path)
