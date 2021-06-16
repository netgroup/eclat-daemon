EXTERNAL_MAKEFILE_PATH= "hike_v3/external/Makefile"
HIKE_SOURCE_PATH = "hike_v3/src/"
HIKE_CC = "hike_v3/hike-tools/hikecc.sh"
BUILD_DIR = "runtime/output/"
LOAD_DIR = "runtime/output/build/"

BPF_FS_PATH = "/sys/fs/bpf/"
TRACE_FS_PATH = "/sys/kernel/tracing"
BPF_FS_PROGS_PATH = BPF_FS_PATH + "progs"
BPF_FS_MAPS_PATH = BPF_FS_PATH + "maps"

# LEXER
TOKEN_MAP_FILE = "parser/syntax/python9-tokens.csv"

# AST
HIKE_DATA_LIST = "runtime/hike_programs_ids.csv"
ECLAT_DATA = "runtime/buildin_eclat_function/"
HIKE_PROGRAM = "runtime/hike_program/"
HIKE_REGISTRY = "runtime/registry.csv"