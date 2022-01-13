COMPONENTS_DIR = 'components'
LOADERS_DIR = f"{COMPONENTS_DIR}/loaders"
PROGRAMS_DIR = f"{COMPONENTS_DIR}/programs"
CHAINS_DIR = f"{COMPONENTS_DIR}/chains"

BUILD_DIR = 'build'
BUILD_LOADERS_DIR = f"{BUILD_DIR}/{COMPONENTS_DIR}/loaders"
BUILD_PROGRAMS_DIR = f"{BUILD_DIR}/{COMPONENTS_DIR}/programs"
BUILD_CHAINS_DIR = f"{BUILD_DIR}/{COMPONENTS_DIR}/chains"

BPF_FS_PATH = "/sys/fs/bpf"
TRACE_FS_PATH = "/sys/kernel/tracing"
BPF_FS_PROGS_PATH = f"{BPF_FS_PATH}/progs"
BPF_FS_MAPS_PATH = f"{BPF_FS_PATH}/maps"
BPF_FS_MAPS_SYSTEM_PATH = f"{BPF_FS_MAPS_PATH}/system"

SYSTEM_MAPS_NAMES = ["hvm_cdata_map",
                     "hvm_chain_map", "hvm_hprog_map", "hvm_shmem_map"]

PROGRAMS_REGISTER_MAP = f"{BPF_FS_MAPS_SYSTEM_PATH}/hvm_hprog_map"
HIKE_CHAIN_MAPS = f"{BPF_FS_MAPS_SYSTEM_PATH}/hike_chain_map"

HIKE_PATH = "hike_v3"
HIKE_SOURCE_PATH = f"{HIKE_PATH}/src"
HIKE_CONTRIB_SOURCE_PATH = f"{HIKE_PATH}/contrib-src"

REPOSITORY_URL = "http://eclat.netgroup.uniroma2.it:3000/v1/package"
PROGRAMS_REPOSITORY_URL = f"{REPOSITORY_URL}/programs"
LOADERS_REPOSITORY_URL = f"{REPOSITORY_URL}/loaders"
CHAINS_REPOSITORY_URL = f"{REPOSITORY_URL}/chains"
