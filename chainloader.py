import json
import cal
import settings
import os


class ChainLoader:
    """
    Loader is responsible for starting the process, setting the initial chain.
    """

    def __init__(self, name, package, configuration={}):
        self.name = name
        self.package = package  # can be the (file) name of the script
        self.configuration = configuration
        ###
        self.maps = []
        self.src_file_path = f"{settings.LOADERS_DIR}/{self.package}/{name}.bpf.c"
        self.obj_file_path = f"{settings.BUILD_LOADERS_DIR}/{self.package}/{name}.bpf.o"
        # TODO Andrea
        self.json_file_path = f"{settings.BUILD_LOADERS_DIR}/{self.package}/{name}.bpf.json"
        self.is_compiled = self._is_compiled()

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

    def _get_maps(self):
        # get the maps
        # here we should parse 1) map name; 2) list primitive data composing the key; 3) list of primitive data composing the value
        # e.g.: {'map_name': 'test', 'key_types': ['u8', 'u16']'key_types': ['u8', 'u16']}
        with open(self.json_file_path) as f:
            data = json.load(f)
            for type in data['types']:
                if type['kind'] == 'STRUCT' and type['name'].startswith("__hike_map_export__"):
                    map_name = type['members'][1]['name']
                    self.maps.append(map_name)

    def pull(self):
        # TODO
        return

    def compile(self):
        if not os.path.exists(self.src_file_path):
            raise Exception(
                f"Compilation failed. File {self.src_file_path} does not exist.")
        if not self.is_compiled:
            cal.make_ebpf_hike_program(self.src_file_path)
            self.is_compiled = True
        else:
            print(f"Chain loader {self.name} is already compiled")

    def clean(self):
        if os.path.exists(self.obj_file_path):
            os.remove(self.obj_file_path)
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)
        self.is_compiled = False

    def write_map(self, map_name, key, data):
        assert(map_name in self.maps)
        # as for now, key and data are provided as array of hex
        # e.g.
        # bpftool map update pinned /sys/fs/bpf/maps/init/map_ipv6		\
        #    key hex		fc 02 00 00 00 00 00 00 00 00 00 00 00 00 00 02 \
        #    value hex 	4f 00 00 00

        # key and data are tuples of primitive data
        full_map_name = f"{settings.BPF_FS_MAPS_PATH}/{self.package}/{self.name}/{map_name}"
        cal.bpftool_map_update(full_map_name, key, data)

    def read_map(self, map_name, key):
        pass

    def load(self):
        if not self.is_compiled:
            raise Exception("Can not load a uncompiled program")
        # Multiple programs may use the same maps. Not implemented now.
        pinned_maps = {}

        map_dir = f"{settings.BPF_FS_MAPS_PATH}/{self.package}"
        cal.bpftool_prog_load(name=self.name, package=self.package,
                              pinned_maps=pinned_maps, is_loader=True)
        self._get_maps()

    def unload(self):
        raise NotImplemented("Unload not implemented")

    def attach(self, dev_name, attach_type="xdp"):
        # name of the section must be equal to the name of the classifier
        pinned_file = f"{settings.BPF_FS_PROGS_PATH}/{self.package}/{self.name}"
        cal.bpftool_net_attach(attach_type, dev_name, pinned_file)

    def detach(self):
        raise NotImplemented("Unregister not implemented")
