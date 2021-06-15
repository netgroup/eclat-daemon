"""
Command Abstraction System
"""
from typing import Coroutine
import settings
import subprocess
import os

# References: 
# - https://manpages.ubuntu.com/manpages/focal/man8/bpftool-prog.8.html
# - https://man.archlinux.org/man/bpftool.8.en



def init_system():
    """
    assert(esiste /sys/fs/bpf/ e /sys/fs/tracefs) 
    mount bpf e tracefs
    mkdir /sys/fs/bpf/progs
    mkdir /sys/fs/bpf/maps
    """
    mount_bpf(settings.BPF_FS_PATH)

    mount_tracefs(settings.TRACE_FS_PATH)

    os.system(f"mkdir {settings.BPF_FS_PROGS_PATH}")
    
    os.system(f"mkdir {settings.BPF_FS_MAPS_PATH}")

    # To get the output of the shell command
    # out = subprocess.Popen(['mkdir', settings.BPF_FS_PROGS_PATH, ], 
    #        stdout=subprocess.PIPE, 
    #        stderr=subprocess.STDOUT)
    # stdout,stderr = out.communicate()



    # TODO Load of Classifier here ???

    # Load all the classifiers
	# bpftool prog loadall classifier.o /sys/fs/bpf/progs/init type xdp \
	#	pinmaps /sys/fs/bpf/maps/init

    # how do we decide which classifier to load?
    # bpftool_prog_load_loadall()


def mount_bpf(mount_point):
    """
    mount -t bpf bpf /sys/fs/bpf/
    """
    # Everything that is private to the bash process that will be launch
    # mount the bpf filesystem.
    # Note: childs of the launching (parent) bash can access this instance
    # of the bpf filesystem. If you need to get access to the bpf filesystem
    # (where maps are available), you need to use nsenter with -m and -t
    # that points to the pid of the parent process (launching bash).
    cmd = f"mount -t bpf bpf {mount_point}"
    os.system(cmd)

def mount_tracefs(mount_point):
    """
    mount -t tracefs nodev /sys/kernel/tracing
    """
    cmd = f"mount -t tracefs nodev {mount_point}"
    os.system(cmd)


def make_hike_chain(makefile, source, hike_dir):
    """
    Run makefile to create an HIKe chain.
    $ make -f path-to/hike_vm/external/Makefile -j24 chain CHAIN=chain.hike.c HIKE_DIR=path-to/hike_vm/src/
    """
    build_dir = settings.BUILD_DIR
    # We just need the name of the object file
    source = source.split("/")[-1]

    # BUILD indicates the path where the compiled file is put and NOT the path of the input file
    # In external MakeFile, $(shell pwd) is executed to get the path:
    ## export OUTPUT := $(abspath $(shell pwd)/$(BUILD))
    # do we need to change folder ???
    currentDirectory = os.getcwd()
    os.chdir(build_dir)

    #cmd = f"make -f {makefile} chain CHAIN={source} HIKE_DIR={hike_dir} BUILD={build_dir}"
    cmd = f"make -f {makefile} chain CHAIN={source} HIKE_DIR={hike_dir}"
    os.system(cmd)

    # reset directory
    os.chdir(currentDirectory)
    
    # unittest
    return True


def make_ebpf_hike_program(makefile, source, hike_dir):
    """
    Run makefile to create an eBPF/HIKe program.
    $ make -f path-to/hike_vm/external/Makefile -j24 prog PROG=prog.bpf.c HIKE_DIR=path-to/hike_vm/src/
    """
    build_dir = settings.BUILD_DIR
    # We just need the name of the object file
    source = source.split("/")[-1]

    # BUILD indicates the path where the compiled file is put and NOT the path of the input file
    # In external MakeFile, $(shell pwd) is executed to get the path:
    ## export OUTPUT := $(abspath $(shell pwd)/$(BUILD))
    # do we need to change folder ???
    currentDirectory = os.getcwd()
    os.chdir(build_dir)

    #cmd = f"make -f {makefile} prog PROG={source} HIKE_DIR={hike_dir} BUILD={build_dir}"
    cmd = f"make -f {makefile} prog PROG={source} HIKE_DIR={hike_dir}"
    os.system(cmd)

    # reset directory
    os.chdir(currentDirectory)

    return True


def hikecc(path_eclat_output, map_name):
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
    # We just need the name of the object file
    map_name = settings.BPF_FS_MAPS_PATH + "/" + map_name
    path_eclat_output = path_eclat_output.split("/")[-1]

    loader_file = path_eclat_output[:-1] + "load.sh"
    hikecc_file = settings.HIKE_CC
    cmd = f"/bin/bash {hikecc_file} {settings.LOAD_DIR + path_eclat_output} " \
            + f"{map_name} {settings.LOAD_DIR + loader_file}"
    os.system(cmd)

    return settings.LOAD_DIR + loader_file
    

def load_chain(loader_file):
    cmd = f"/bin/bash {loader_file}"
    os.system(cmd)
    #unittest
    return True


# bpftool prog { load | loadall } OBJ PATH [type TYPE] 
## [map {idx IDX |  name  NAME}  MAP] [dev NAME] [pinmaps MAP_DIR]
def bpftool_prog_loadall(prog_obj, prog_path, type=None, map_idx=None, map_name=None, 
                        map_map=None, dev_name=None, pinmaps_map_dir=None):
    command = "bpftool prog loadall " + prog_obj + " " + prog_path + " "
    command += bpftool_prog_load_loadall(type, map_idx, map_name, map_map, dev_name, pinmaps_map_dir)
    os.system(command)

    #unittest
    return True

# bpftool prog { load | loadall } OBJ PATH [type TYPE] 
## [map {idx IDX |  name  NAME}  MAP] [dev NAME] [pinmaps MAP_DIR]
def bpftool_prog_load(prog_obj, prog_path, type=None, map_idx=None, map_name=None, 
                        map_map=None, dev_name=None, pinmaps_map_dir=None):
    command = "bpftool prog load " + prog_obj + " " + prog_path + " "
    command += bpftool_prog_load_loadall(type, map_idx, map_name, map_map, dev_name, pinmaps_map_dir)
    os.system(command)

    #unittest
    return True

def bpftool_prog_load_loadall(type=None, map_idx=None, map_name=None, 
                        map_map=None, dev_name=None, pinmaps_map_dir=None):
    command = ""
    if type:
        command += " type " + type + " "

    if map_idx:
        command += " map idx " + map_idx + " pinned " + map_map
    elif map_name:
        command += " map name " + map_name + " pinned " + map_map

    if dev_name:
        command += " dev " + dev_name + " "

    if pinmaps_map_dir:
        command += " pinmaps " + pinmaps_map_dir
    return command


# bpftool net attach ATTACH_TYPE PROG dev NAME [ overwrite ]
# bpftool net detach ATTACH_TYPE dev NAME
##### PROG := {id PROG_ID | pinned FILE | tag PROG_TAG}
##### ATTACH_TYPE := {xdp | xdpgeneric | xdpdrv | xdpoffload}
def bpftool_net_attach(attach_type, dev_name, prog=None, flag_overwrite=None):
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

    os.system(command)



# bpftool map update MAP [key DATA] [value VALUE] [UPDATE_FLAGS]
##### MAP := {id MAP_ID | pinned FILE | name MAP_NAME}
##### DATA := {[hex] BYTES}
##### VALUE := {DATA | MAP | PROG}
##### UPDATE_FLAGS := {any | exist | noexist}
def bpftool_map_update(map_map, key_data=None, value=None, update_flags=None):
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
        
    os.system(command)

    #unittest
    return True