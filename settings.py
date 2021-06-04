EXTERNAL_MAKEFILE_PATH= "hike_v3/external/Makefile"
HIKE_SOURCE_PATH = "hike_v3/src/"
HIKE_CC = "hike_v3/hike-tools/hikecc.sh"
BUILD_DIR = "runtime/output/"
LOAD_DIR = "runtime/output/build/"
MAP_PATH = "/sys/fs/bpf/maps/hike_chain_map"

BPF_FS_PATH = "/sys/fs/bpf/"
TRACE_FS_PATH = "/sys/kernel/tracing"
BPF_FS_PROGS_PATH = BPF_FS_PATH + "progs"
BPF_FS_MAPS_PATH = BPF_FS_PATH + "maps"

# AST
HIKE_DATA_LIST = "runtime/hike_programs_ids.csv"
ECLAT_DATA = "runtime/buildin_eclat_function/"
HIKE_PROGRAM = "runtime/hike_program/"
HIKE_REGISTRY = "runtime/registry.csv"