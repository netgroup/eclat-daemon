import json
import struct
import settings
import os
import cal
from package_manager import PackageManager
from parser.json_parser import parse_info, flatten, get_type_fmt
from test.package_manager import PackageManager


class HikeProgram:
    """
    An HIKe Program is a conventional eBPF program which can be re-used in multiple composition schemes.
    An HIKe program should return the control to the HIKe VM.
    """

    def __init__(self, name, package):
        self.name = name
        self.package = package
        ###
        self.maps = []
        if self.package == 'hike_default':
            # this is an exception to keep the repo with the basic set of hike programs untouched
            self.src_file_path = f"{settings.HIKE_SOURCE_PATH}/{name}.bpf.c"
            self.obj_file_path = f"{settings.HIKE_SOURCE_PATH}/.output/{name}.bpf.o"
            self.json_file_path = f"{settings.HIKE_SOURCE_PATH}/.output/{name}.bpf.json"
        else:
            self.src_file_path = f"{settings.COMPONENTS_DIR}/{self.package}/{name}.bpf.c"
            self.obj_file_path = f"{settings.COMPONENTS_DIR}/{self.package}/build/{name}.bpf.o"
            self.json_file_path = f"{settings.COMPONENTS_DIR}/{self.package}/build/{name}.bpf.json"

        self.program_path = f"{settings.BPF_FS_PROGS_PATH}/{self.package}/{self.name}"
        self.is_compiled = self._is_compiled()
        self.program_id = None

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

    def _get_maps(self):
        # get the maps
        # [{'map_name': 'ipv6_hset_srcdst_map', 'key_type': [[('byte_array', 16)], [('byte_array', 16)]], 'value_type': [('int', 64), ('int', 64)]}]
        # hike_program_info = {'param_num': 2, 'param_types': [('int', 32), ('int', 64)]}

        (maps_info, hike_program_info) = parse_info(self.json_file_path)
        self.maps_info = maps_info
        self.program_info = hike_program_info
        return maps_info

    def pull(self):
        pm = PackageManager()
        pm.pull(self.package)

    def compile(self):
        if not os.path.exists(self.src_file_path):
            raise Exception(
                f"Compilation failed. File {self.src_file_path} does not exist.")
        build_dir = None
        if self.package == 'hike_default':
            build_dir = '.output'
        cal.make_ebpf_hike_program(self.src_file_path, build_dir)
        self.is_compiled = True
        # else:
        #    print(f"Hike program {self.name} is already compiled")

    def clean(self):
        if os.path.exists(self.obj_file_path):
            os.remove(self.obj_file_path)
        if os.path.exists(self.json_file_path):
            os.remove(self.json_file_path)
        self.is_compiled = False

    def load(self):
        if not self.is_compiled:
            raise Exception("Can not load a uncompiled program")
        # Multiple programs may use the same maps. Not implemented now.
        pinned_maps = {}

        map_dir = f"{settings.BPF_FS_MAPS_PATH}/{self.package}"
        cal.bpftool_prog_load(name=self.name, package=self.package,
                              pinned_maps=pinned_maps, obj_file=self.obj_file_path)
        self._get_maps()

    def unload(self):
        raise NotImplemented("Unload not implemented")

    def register(self, program_id):
        if not self.is_compiled:
            raise Exception("Can not register a uncompiled program")
        key_values = ['{0:02x}'.format(program_id), '00', '00', '00']
        cal.bpftool_map_update(
            settings.PROGRAMS_REGISTER_MAP, key_values, self.program_path)

    def unregister(self):
        raise NotImplemented("Unregister not implemented")

    def write_map(self, map_name, key, data):

        map_info = filter(lambda x: x['map_name'] == map_name, self.maps_info)
        assert(len(map_info) == 1)
        key_types = flatten(map_info['key_type'])
        value_types = flatten(map_info['value_type'])
        key_bytes = struct.pack(get_type_fmt(key_types), key)
        val_bytes = struct.pack(get_type_fmt(key_types), key)

        key_data_string = (" ".join(hex(n)
                           for n in key_bytes)).replace('0x', '')
        value_data_string = (" ".join(hex(n)
                             for n in key_bytes)).replace('0x', '')

        # [{'map_name': 'ipv6_hset_srcdst_map', 'key_type': [[('byte_array', 16)], [(
        #    'byte_array', 16)]], 'value_type': [('int', 64), ('int', 64)]}]

        # as for now, key and data are provided as array of hex
        # e.g.
        # bpftool map update pinned /sys/fs/bpf/maps/init/map_ipv6		\
        #    key hex		fc 02 00 00 00 00 00 00 00 00 00 00 00 00 00 02 \
        #    value hex 	4f 00 00 00

        full_map_name = f"{settings.BPF_FS_MAPS_PATH}/{self.package}/{self.name}/{map_name}"
        cal.bpftool_map_update(
            full_map_name, key_data_string, value_data_string)

    def read_map(self, map_name, key):
        pass

    def get_maps(self):
        pass
