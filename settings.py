COMPONENTS_DIR = 'components'

BPF_FS_PATH = "/sys/fs/bpf"
TRACE_FS_PATH = "/sys/kernel/tracing"
BPF_FS_PROGS_PATH = f"{BPF_FS_PATH}/progs"
BPF_FS_MAPS_PATH = f"{BPF_FS_PATH}/maps"
BPF_FS_MAPS_SYSTEM_PATH = f"{BPF_FS_MAPS_PATH}/system"

SYSTEM_MAPS_NAMES = ["hvm_cdata_map",
                     "hvm_chain_map", "hvm_hprog_map", "hvm_shmem_map"]

PROGRAMS_REGISTER_MAP = f"{BPF_FS_MAPS_SYSTEM_PATH}/hvm_hprog_map"
HIKE_CHAIN_MAPS = f"{BPF_FS_MAPS_SYSTEM_PATH}/hike_chain_map"

HIKE_PATH = "hike"
HIKE_SOURCE_PATH = f"{HIKE_PATH}/src"
HIKE_CONTRIB_SOURCE_PATH = f"{HIKE_PATH}/contrib-src"

REPOSITORY_URL = "http://eclat.netgroup.uniroma2.it:3000/v1/package"

PROGRAMS_REPOSITORY_URL = f"{REPOSITORY_URL}"
LOADERS_REPOSITORY_URL = f"{REPOSITORY_URL}"
CHAINS_REPOSITORY_URL = f"{REPOSITORY_URL}"

LOG_CONFIG = {
    "version":1,
    "root":{
        "handlers" : ["console", "file"],
        "level": "DEBUG"
    },
    "handlers":{
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "file":{
            "formatter":"std_out",
            "class":"logging.FileHandler",
            "level":"DEBUG",
            "filename":"log/eclatd.log"
        }
    },
    "formatters":{
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(lineno)d : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    },
}
