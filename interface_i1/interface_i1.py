# References: 
# - https://manpages.ubuntu.com/manpages/focal/man8/bpftool-prog.8.html
# - https://man.archlinux.org/man/bpftool.8.en

# bpftool prog { load | loadall } OBJ PATH [type TYPE] 
## [map {idx IDX |  name  NAME}  MAP] [dev NAME] [pinmaps MAP_DIR]
from typing import Coroutine


def prog_load_all(load_loadall, prog_obj, prog_path, 
                    type=None, map_idx=None, map_name=None, 
                        map_map=None, dev_name=None, pinmaps_map_dir=None):
    # load_loadall = "load" or "loadall" 
    command = "bpftool prog " + load_loadall + prog_obj + " " + prog_path + " "
    # Fixed Path???: command += ... +"/sys/fs/bpf/progs" + ...
    if type != None:
        command += "type" + type + " "

    if map_idx != None:
        command += "map idx" + map_idx + " " + map_map
    elif map_name != None:
        command += "map name" + map_name + " " + map_map

    if dev_name != None:
        command += "dev" + dev_name + " "

    if pinmaps_map_dir != None:
        command += "pinmaps" + pinmaps_map_dir
    
    return command



# bpftool net attach ATTACH_TYPE PROG dev NAME [ overwrite ]
# bpftool net detach ATTACH_TYPE dev NAME
##### PROG := {id PROG_ID | pinned FILE | tag PROG_TAG}
##### ATTACH_TYPE := {xdp | xdpgeneric | xdpdrv | xdpoffload}
def net_attach(attach_type, dev_name, prog=None, flag_overwrite=None):
    command = ""
    if attach_type in ["xdp", "xdpgeneric", "xdpdrv", "xdpoffload"]:
        command += "bpftool net attach" + attach_type + " " 
    else:
        #Placeholder
        print("ERRORE")

    if prog != None:
        if prog.split(" ")[0] in ["id", "pinned", "tag"]:
            command += prog + " "
        else:
            #Placeholder
            print("ERRORE")

    command += dev_name + " "

    if flag_overwrite != None:
        command += flag_overwrite

    return command



# bpftool map update MAP [key DATA] [value VALUE] [UPDATE_FLAGS]
##### MAP := {id MAP_ID | pinned FILE | name MAP_NAME}
##### DATA := {[hex] BYTES}
##### VALUE := {DATA | MAP | PROG}
##### UPDATE_FLAGS := {any | exist | noexist}
def map_update(map_map, key_data=None, value=None, update_flags=None):
    command = ""
    if map_map.split(" ")[0] in ["id", "pinned", "tag"]:
        command = "bpftool map update" + map_map + " "
    else:
        #Placeholder
        print("ERRORE")

    if key_data != None:
        command += "key"
        if key_data.split(" ")[0] == "hex":
            try:
                int(key_data.split(" ")[1], 16)
                #Placeholder
                print('That is a valid hex value.')
            except:
                #Placeholder
                print('That is an invalid hex value.')
            command += "hex" + " "
        command += key_data + " "

    if value != None:
        command += "value" + value + " "
    
    if update_flags in ["any", "exist", "noexist"]:
        command += update_flags + " "
    else:
        #Placeholder
        print("ERRORE")
        
    return command




"""
# Everything that is private to the bash process that will be launch
# mount the bpf filesystem.
# Note: childs of the launching (parent) bash can access this instance
# of the bpf filesystem. If you need to get access to the bpf filesystem
# (where maps are available), you need to use nsenter with -m and -t
# that points to the pid of the parent process (launching bash).

mount -t bpf bpf /sys/fs/bpf/
mount -t tracefs nodev /sys/kernel/tracing

mkdir /sys/fs/bpf/progs
mkdir /sys/fs/bpf/maps
"""
def mount(path, bpf_tracefs):
    command = "mount -t "
    if bpf_tracefs == "bpf":
        command += "bpf bpf "
    else:
        command += "tracefs nodev "
    command += path

    return command   


def mkdir(path):
    return "mkdir" + path 


"""
For compiling an eBPF/HIKe Program:
 $ make -f path-to/hike_vm/external/Makefile -j24 prog PROG=prog.bpf.c HIKE_DIR=path-to/hike_vm/src/

For compiling an HIKe Chain:
 $ make -f path-to/hike_vm/external/Makefile -j24 chain CHAIN=chain.hike.c HIKE_DIR=path-to/hike_vm/src/
"""  
def make(path_makefile, flag_prog_chain, prog_chain_name, hike_dir_path):
    command = "make -f " + path_makefile + " "
    if flag_prog_chain == "prog":
        command += flag_prog_chain + " PROG=" + prog_chain_name + ".bpf.c "
    else:
        command += flag_prog_chain + " CHAIN=" + prog_chain_name + ".hike.c "
    command += "HIKE_DIR=" + hike_dir_path
    return command


"""
# The HIKECC takes as 1) the HIKe Chains object file; 2) the eBPF map
# that contains all the HIKe Chains; 3) the path of the load script
# that is going to be generated.
${HIKECC} data/binaries/minimal_chain.hike.o			\
        /sys/fs/bpf/maps/hike_chain_map 			\
        data/binaries/minimal_chain.hike.load.sh

# Load HIKe Chains calling the loader script we just built :-o
/bin/bash data/binaries/minimal_chain.hike.load.sh
"""
def hikecc(path_eclat_output, path_chain, path_output):
    command = "/bin/bash /opt/hike_v3/hike-tools/hikecc.sh " \
        + path_eclat_output + " " + \
            + path_chain + " " + \
                + path_output
    command += "\n" + "/bin/bash " + path_output
    return command

