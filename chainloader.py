import json
import cal
import settings
import os
import struct
from parser.json_parser import parse_info, flatten, get_type_fmt


class ChainLoader:
    """
    Loader is responsible for starting the process, setting the initial chain.
    """

    def __init__(self, name, package, configuration={}):
        self.name = name
        self.package = package  # can be the (file) name of the script
        self.configuration = configuration
        ###
        self.maps_info = []
        self.src_file_path = f"{settings.LOADERS_DIR}/{self.package}/{name}.bpf.c"
        self.obj_file_path = f"{settings.BUILD_LOADERS_DIR}/{self.package}/{name}.bpf.o"
        # TODO Andrea
        self.json_file_path = f"{settings.BUILD_LOADERS_DIR}/{self.package}/{name}.bpf.json"
        self.is_compiled = self._is_compiled()

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

    def _get_maps(self):
        # get the maps
        # [{'map_name': 'ipv6_hset_srcdst_map', 'key_type': [[('byte_array', 16)], [('byte_array', 16)]], 'value_type': [('int', 64), ('int', 64)]}]
        from parser.json_parser import parse_info, flatten
        (maps_info, hike_program_info) = parse_info(self.json_file_path)
        self.maps_info = maps_info
        return maps_info

    def link(self, maps, registered_ids):
        """Substitute in maps configuration the chain ids

        :param maps: parser maps -> [{'program_name': ..., 'map_name': ..., 'data' {k1: v1, k2: v2}}]
        :param registered_ids: registered ids -> [{type, package, name, id}]
        :return: linked maps
        """
        chain_ids = [(ri['name'], ri['id'])
                     for ri in registered_ids if ri['type'] == 'chain']

        for i, map_info in enumerate(maps):
            for k, vs, in map_info['data'].items():
                for chain_name, chain_id in chain_ids:
                    if chain_name in vs:
                        maps[i]['data'][k] = list(map(
                            lambda x: chain_id if chain_name in x else x, maps[i]['data'][k]))

        return maps

    def pull(self):
        """
        Download a package in the appropriate directory
        """
        import requests
        import tarfile
        # if there is not a folder, download the package
        if not os.path.isdir(f"{settings.LOADERS_DIR}/{self.package}"):
            file_name = f"{self.package}.tar.gz"
            url = f"{settings.LOADERS_REPOSITORY_URL}/{file_name}"
            r = requests.get(url, allow_redirects=True)
            file_path = f"{settings.LOADERS_DIR}/{file_name}"
            open(file_path, 'wb').write(r.content)
            tar = tarfile.open(file_path, "r:gz")
            # this should create the /package_name/ folder
            tar.extractall(settings.LOADERS_DIR)
            tar.close()
            os.remove(file_path)

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

    def write_map(self, map_name, key, value):
        map_info = None
        for mi in self.maps_info:
            if mi['map_name'] == map_name:
                map_info = mi
        assert(map_info)  # map is not exported by the program
        # TODO handle nested maps
        # key_types = flatten(map_info['key_type'])
        # value_types = flatten(map_info['value_type'])

        key_types = map_info['key_type']
        value_types = map_info['value_type']

        # transform keys and data element in integers
        i_key = [int(k) for k in key]
        i_value = [int(k) for k in value]

        key_bytes = struct.pack(get_type_fmt(key_types), *i_key)
        val_bytes = struct.pack(get_type_fmt(value_types), *i_value)

        key_data_string = (" ".join(hex(n)
                           for n in key_bytes)).replace('0x', '')
        value_data_string = (" ".join(hex(n)
                             for n in val_bytes)).replace('0x', '')

        # [{'map_name': 'ipv6_hset_srcdst_map', 'key_type': [[('byte_array', 16)], [(
        #    'byte_array', 16)]], 'value_type': [('int', 64), ('int', 64)]}]

        # as for now, key and data are provided as array of hex
        # e.g.
        # bpftool map update pinned /sys/fs/bpf/maps/init/map_ipv6		\
        #    key hex		fc 02 00 00 00 00 00 00 00 00 00 00 00 00 00 02 \
        #    value hex 	4f 00 00 00

        full_map_name = f"{settings.BPF_FS_MAPS_PATH}/{self.package}/{self.name}/{map_name}"
        cal.bpftool_map_update(
            full_map_name, key_data_string.split(), value_data_string.split(), value_type="hex")

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
