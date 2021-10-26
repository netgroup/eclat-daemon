import cal
import settings
import os


class ChainLoader:
    """
    Loader is responsible for starting the process, setting the initial chain.
    """

    def __init__(self, name, package, configuration):
        self.name = name
        self.package = package  # can be the (file) name of the script
        self.configuration = configuration
        ###
        self.src_file_path = f"{settings.LOADERS_DIR}/{self.package}/{name}.bpf.c"
        self.obj_file_path = f"{settings.BUILD_LOADERS_DIR}/{self.package}/{name}.bpf.o"
        self.is_compiled = self._is_compiled()
        #self.is_linked = self._is_linked()

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

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
        pass

    def read_map(self, map_name, key):
        pass

    def get_maps(self):
        pass

    def load(self):
        if not self.is_compiled:
            raise Exception("Can not load a uncompiled program")
        # Multiple programs may use the same maps. Not implemented now.
        pinned_maps = {}

        map_dir = f"{settings.BPF_FS_MAPS_PATH}/{self.package}"
        cal.bpftool_prog_load(name=self.name, package=self.package,
                              pinned_maps=pinned_maps)

    def unload(self):
        raise NotImplemented("Unload not implemented")

    def attach(self, dev_name):
        # name of the section must be equal to the name of the classifier
        pinned_file = f"{settings.BPF_FS_PROGS_PATH}/{self.package}/{self.name}"
        cal.bpftool_net_attach('xdp', dev_name, pinned_file)

    def detach(self):
        raise NotImplemented("Unregister not implemented")
