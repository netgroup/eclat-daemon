"""
Command Abstraction Layer
"""
from typing import Coroutine
import settings
import subprocess
import os

# References:
# - https://manpages.ubuntu.com/manpages/focal/man8/bpftool-prog.8.html
# - https://man.archlinux.org/man/bpftool.8.en


def ebpf_system_init():
    """
    mount bpf and tracefs
    mkdir /sys/fs/bpf/progs
    mkdir /sys/fs/bpf/maps
    """
    mount_bpf(settings.BPF_FS_PATH)
    mount_tracefs(settings.TRACE_FS_PATH)

    mkdir(settings.BPF_FS_PROGS_PATH)
    mkdir(settings.BPF_FS_MAPS_PATH)

    mkdir(settings.BUILD_LOADERS_DIR)
    mkdir(settings.BUILD_PROGRAMS_DIR)
    mkdir(settings.BUILD_CHAINS_DIR)


def hike_system_init():
    """
    Initialize HIKe system by loading HIKe maps.
    """
    import settings

    # It allows to load maps with many entries without failing
    if os.system("ulimit -l unlimited"):
        raise OSError(f"Failing in setting user limit to unlimited")

    # load a "dummy" classifier to load the maps

    # make -f hike_v3/external/Makefile -j24 prog PROG=components/loaders/init_hike.bpf.c HIKE_DIR=hike_v3/src/
    if not os.path.exists("/sys/fs/bpf/progs/system"):
        bpf_source_file = os.path.join(
            settings.PROGRAMS_DIR, 'system/init_hike.bpf.c')  # TODO

        make_ebpf_hike_program(bpf_source_file)

        # bpf_output_file = os.path.join(
        #    settings.BUILD_PROGRAMS_DIR, 'init_hike.bpf.o')

        pinned_maps = {}
        bpftool_prog_load("init_hike", "system", pinned_maps,
                          load_system_maps=False)
        print("Init program loaded")


def mkdir(path):
    """
    mkdir path
    """
    cmd = f"mkdir -p {path}"
    ret = os.system(cmd)
    if ret:
        raise OSError(f"Can not create directory {path}")


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
    cmd = f"grep -qs '{mount_point} ' /proc/mounts || mount -t bpf bpf {mount_point}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret:
        raise OSError(f"Can not mount BPF fs on {mount_point}")


def mount_tracefs(mount_point):
    """
    mount -t tracefs nodev /sys/kernel/tracing
    """
    cmd = f"grep -qs '{mount_point} ' /proc/mounts || mount -t tracefs nodev {mount_point}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret:
        raise OSError(f"Can not mount trace fs on {mount_point}")


def make_hike_chain(file_path):
    """
    Run makefile to create an HIKe chain.
    $ make -f path-to/hike_vm/external/Makefile -j24 chain CHAIN=chain.hike.c HIKE_DIR=path-to/hike_vm/src/
    """
    makefile = f"{settings.HIKE_PATH}/external/Makefile"
    cmd = f"make -f {makefile} chain CHAIN={file_path} HIKE_DIR={settings.HIKE_SOURCE_PATH}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(
            f"Hike Chain compilation failed\nOffending command is {cmd}")


def make_ebpf_hike_program(file_path):
    """
        Compile the eBPF HIKe program specified in the file_path
        $ make -f path-to/hike_vm/external/Makefile -j24 prog PROG=prog.bpf.c HIKE_DIR=path-to/hike_vm/src/
    """
    makefile = f"{settings.HIKE_PATH}/external/Makefile"
    cmd = f"make -f {makefile} prog PROG={file_path} HIKE_DIR={settings.HIKE_SOURCE_PATH}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(
            f"Hike Program compilation failed\nOffending command is {cmd}")


# def make_ebpf_hike_program(makefile, source, hike_dir):
#     """
#     Run makefile to create an eBPF/HIKe program.
#     $ make -f path-to/hike_vm/external/Makefile -j24 prog PROG=prog.bpf.c HIKE_DIR=path-to/hike_vm/src/
#     """
#     build_dir = settings.BUILD_DIR
#     # We just need the name of the object file
#     source = source.split("/")[-1]

#     # BUILD indicates the path where the compiled file is put and NOT the path of the input file
#     # In external MakeFile, $(shell pwd) is executed to get the path:
#     # export OUTPUT := $(abspath $(shell pwd)/$(BUILD))
#     # do we need to change folder ???
#     currentDirectory = os.getcwd()
#     os.chdir(build_dir)

#     #cmd = f"make -f {makefile} prog PROG={source} HIKE_DIR={hike_dir} BUILD={build_dir}"
#     cmd = f"make -f {makefile} prog PROG={source} HIKE_DIR={hike_dir}"
#     os.system(cmd)

#     # reset directory
#     os.chdir(currentDirectory)

#     return True


def hikecc(name, package):
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
    obj_file_path = f"{settings.BUILD_CHAINS_DIR}/{package}/{name}.hike.o"
    map_name = f"{settings.BPF_FS_MAPS_SYSTEM_PATH}/hike_chain_map"
    loader_file_path = f"{settings.BUILD_CHAINS_DIR}/{package}/{name}.hike.load.sh"
    HIKE_CC = f"{settings.HIKE_PATH}/hike-tools/hikecc.sh"

    cmd = f"/bin/bash {HIKE_CC} {obj_file_path} {map_name} {loader_file_path}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(
            f"HikeCC Chain loader creation failed\nOffending command is {cmd}")
    load_chain(loader_file_path)


def load_chain(loader_file):

    cmd = f"/bin/bash {loader_file}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(
            f"HikeCC Chain loader execution failed\nOffending command is {cmd}")


def bpftool_prog_load(name, package,
                      pinned_maps, attach_type="xdp", load_system_maps=True, is_loader=False):
    """Use BPF tool to load one section

    :param name: name of the program
    :param package: package name
    :param pinned_maps: dictionary of map (name and sys/fs dir) other than the SYSTEM_MAPS_NAMES
    :param attach_type: interface name, defaults to "xdp"
    :param is_loader: whether referring to the load of a program or of a chain loader
    """
    # bpftool prog loadall net.o /sys/fs/bpf/progs/net type xdp	\
    #             map name gen_jmp_table					\
    #                     pinned	/sys/fs/bpf/maps/init/gen_jmp_table	\
    #             map name hike_chain_map					\
    #                     pinned /sys/fs/bpf/maps/init/hike_chain_map 	\
    #             map name pcpu_hike_chain_data_map			\
    #                     pinned /sys/fs/bpf/maps/init/pcpu_hike_chain_data_map \
    #             map name hike_pcpu_shmem_map				\
    #                     pinned /sys/fs/bpf/maps/init/hike_pcpu_shmem_map \
    #             pinmaps /sys/fs/bpf/maps/net

    program_object_prefix = settings.BUILD_PROGRAMS_DIR if is_loader == False else settings.BUILD_LOADERS_DIR
    program_object = f"{program_object_prefix}/{package}/{name}.bpf.o"
    program_fs_path = f"{settings.BPF_FS_PROGS_PATH}/{package}/{name}"
    program_maps_fs_path = f"{settings.BPF_FS_MAPS_PATH}/{package}"

    mkdir(f"{settings.BPF_FS_PROGS_PATH}/{package}")
    mkdir(program_maps_fs_path)
    if os.path.exists(program_fs_path):
        print(f"{name} is already loaded")
        return

    cmd = f"bpftool prog load {program_object} {program_fs_path} type {attach_type} "
    for k, v in pinned_maps:
        cmd += f"map name {k} pinned {v} "
    if load_system_maps:
        for system_map_name in settings.SYSTEM_MAPS_NAMES:
            cmd += f"map name {system_map_name} pinned {settings.BPF_FS_MAPS_SYSTEM_PATH}/{system_map_name} "
    cmd += f" pinmaps {program_maps_fs_path}"
    print(f"Exec: {cmd}")
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(f"Program {program_object} load failed.")


# bpftool net attach ATTACH_TYPE PROG dev NAME [ overwrite ]
# bpftool net detach ATTACH_TYPE dev NAME
# PROG := {id PROG_ID | pinned FILE | tag PROG_TAG}
# ATTACH_TYPE := {xdp | xdpgeneric | xdpdrv | xdpoffload}
def bpftool_net_attach(attach_type, dev_name, pinned_file):
    if not attach_type in ["xdp", "xdpgeneric", "xdpdrv", "xdpoffload"]:
        raise NotImplemented("Attach type not supported")

    cmd = f"bpftool net attach {attach_type} pinned {pinned_file} dev {dev_name}"
    print(cmd)
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(
            f"Bpftool net attach of {pinned_file} on dev {dev_name} failed.")

# bpftool map update MAP [key DATA] [value VALUE] [UPDATE_FLAGS]
# MAP := {id MAP_ID | pinned FILE | name MAP_NAME}
# DATA := {[hex] BYTES}
# VALUE := {DATA | MAP | PROG}
# UPDATE_FLAGS := {any | exist | noexist}
# bpftool map update pinned /sys/fs/bpf/maps/init/gen_jmp_table 	\
#		key	hex 0b 00 00 00					\
#		value	pinned /sys/fs/bpf/progs/net/hvxdp_allow_any


# bpftool map update id <id> key <key> value <new_value>
# bpftool map update pinned <path> key <key> value <new_value>
def bpftool_map_update(map_reference, key, value, map_reference_type="pinned"):
    """Update a eBPF map

    :param map_reference: ID of the map or sys/fs path if reference refers to a pinned map
    :param key: key to update (passed as list of hex)
    :param value: value to be written
    :param map_reference_type: id or pinned, defaults to "pinned"
    """
    if map_reference_type == "pinned":
        key_string = " ".join(key)
        cmd = f"bpftool map update pinned {map_reference} key hex {key_string} value pinned {value}"
    else:
        raise Exception("bpftool_map_update: Instruction not implemented.")

    print(f"Exec: {cmd}")
    ret = os.system(cmd)

    if ret != 0:
        raise Exception(f"Map update {map_reference} failed.")

    # unittest
    return True


# # bpftool map update MAP [key DATA] [value VALUE] [UPDATE_FLAGS]
# # MAP := {id MAP_ID | pinned FILE | name MAP_NAME}
# # DATA := {[hex] BYTES}
# # VALUE := {DATA | MAP | PROG}
# # UPDATE_FLAGS := {any | exist | noexist}
# def bpftool_map_update(map_map, key_data=None, value=None, update_flags=None):
#     cmd = ""
#     if map_map.split(" ")[0] in ["id", "pinned", "tag"]:
#         cmd = "bpftool map update" + map_map + " "
#     else:
#         # Placeholder
#         raise Exception("bpftool_map_update: Instruction not implemented.")

#     if key_data != None:
#         cmd += "key"
#         if key_data.split(" ")[0] == "hex":
#             try:
#                 int(key_data.split(" ")[1], 16)
#                 # Placeholder
#                 print('That is a valid hex value.')
#             except:
#                 # Placeholder
#                 print('That is an invalid hex value.')
#             cmd += "hex" + " "
#         cmd += key_data + " "

#     if value != None:
#         cmd += "value" + value + " "

#     if update_flags in ["any", "exist", "noexist"]:
#         cmd += update_flags + " "
#     else:
#         # Placeholder
#         print("ERRORE")

#     print(f"Exec: {cmd}")
#     ret = os.system(cmd)

#     # unittest
#     return True
