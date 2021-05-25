import os
from eCLAT_Code.Code.path import Path

def allow():
    path = Path.import_path + "hike_program/allow.c"
    if os.path.exists(path):
        return path
        #return "eCLAT_Code/Code/Lib/hike/allow.c"

def bar():
    path = Path.import_path + "hike_program/bar.c"
    if os.path.exists(path):
        return path
        #return "eCLAT_Code/Code/Lib/hike/bar.c"

def drop():
    path = Path.import_path + "hike_program/drop.c"
    if os.path.exists(path):
        return path
    #return "eCLAT_Code/Code/Lib/hike/drop.c"

def fast():
    path = Path.import_path + "hike_program/fast.c"
    if os.path.exists(path):
        return path
    #return "eCLAT_Code/Code/Lib/hike/fast.c"

def mon():
    path = Path.import_path + "hike_program/mon.c"
    if os.path.exists(path):
        return path
    #return "eCLAT_Code/Code/Lib/hike/mon.c"

def parse_ethernet():
    path = Path.import_path + "hike_program/parse_ethernet.c"
    if os.path.exists(path):
        return path
    #return "eCLAT_Code/Code/Lib/hike/parse_ethernet.c"

def slow():
    path = Path.import_path + "hike_program/slow.c"
    if os.path.exists(path):
        return path
    #return "eCLAT_Code/Code/Lib/hike/slow.c"


def get_iflabel_id():
    path = Path.import_path + "hike_program/get_iflabel_id.c"
    if os.path.exists(path):
        return path

def get_time_8_bit():
    path = Path.import_path + "hike_program/get_time_8_bit.c"
    if os.path.exists(path):
        return path


def pkt_mem_move():
    path = Path.import_path + "hike_program/pkt_mem_move.c"
    if os.path.exists(path):
        return path


def interface_load():
    path = Path.import_path + "hike_program/interface_load.c"
    if os.path.exists(path):
        return path


def get_ingress_ifindex():
    path = Path.import_path + "hike_program/get_ingress_ifindex.c"
    if os.path.exists(path):
        return path


