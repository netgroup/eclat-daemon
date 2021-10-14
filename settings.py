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

SYSTEM_MAPS_NAMES = ["gen_jmp_table", "hike_chain_map",
                     "pcpu_hike_chain_data_map", "hike_pcpu_shmem_map"]

PROGRAMS_REGISTER_MAP = f"{BPF_FS_MAPS_SYSTEM_PATH}/gen_jmp_table"

HIKE_PATH = "hike_v3"
HIKE_SOURCE_PATH = f"{HIKE_PATH}/src"

REPOSITORY_URL = "https://www.uniroma2.it/hike/repo/"

########## OLD SETTINGS ###########
# EXTERNAL_MAKEFILE_PATH = "hike_v3/external/Makefile"
# HIKE_SOURCE_PATH = "hike_v3/src/"
# HIKE_CC = "hike_v3/hike-tools/hikecc.sh"
# BUILD_DIR = "runtime/output/"
# LOAD_DIR = "runtime/output/build/"

# BPF_FS_PATH = "/sys/fs/bpf/"
# TRACE_FS_PATH = "/sys/kernel/tracing"
# BPF_FS_PROGS_PATH = BPF_FS_PATH + "progs"
# BPF_FS_MAPS_PATH = BPF_FS_PATH + "maps"

# # LEXER
# TOKEN_MAP_FILE = "parser/syntax/python9-tokens.csv"

# # AST
# HIKE_DATA_LIST = "runtime/hike_programs_ids.csv"
# ECLAT_DATA = "runtime/buildin_eclat_function/"
# HIKE_PROGRAM = "runtime/hike_program/"
# HIKE_REGISTRY = "runtime/registry.csv"
