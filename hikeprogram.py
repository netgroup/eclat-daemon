import settings
import os
import cal


class HikeProgram:
    counter = 11

    def __init__(self, package, program_name):
        self.program_name = program_name
        self.package = package
        ###
        self.src_file_path = f"{settings.PROGRAMS_DIR}/{self.package}/{program_name}.bpf.c"
        self.obj_file_path = f"{settings.BUILD_PROGRAMS_DIR}/{self.package}/{program_name}.bpf.o"
        self.json_file_path = f"{settings.BUILD_PROGRAMS_DIR}/{self.package}/{program_name}.bpf.json"
        self.program_path = f"{settings.BPF_FS_PROGS_PATH}/{self.package}/{self.program_name}"
        self.is_compiled = self._is_compiled()
        self.program_id = self.counter
        HikeProgram.counter += 1

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

    def pull(self):
        """
        [Temporary] download a package in the appropriate directory
        """
        # TODO: handle dependencies. Package manager?
        import requests
        import tarfile

        # if there is not a folder, download the package
        if not os.path.isdir(f"{settings.PROGRAMS_DIR}/{self.package}"):
            file_name = f"{self.package}.tar.gz"
            url = f"{settings.REPOSITORY_URL}/{file_name}"
            r = requests.get(url, allow_redirects=True)
            file_path = f"{settings.PROGRAMS_DIR}/{file_name}"
            open(file_path, 'wb').write(r.content)

            tar = tarfile.open(file_path, "r:gz")
            # this should create the /package_name/ folder
            tar.extractall()
            tar.close()
            # file_name = f"{self.package}.tar.gz"

    def compile(self):
        if not os.path.exists(self.src_file_path):
            raise Exception(
                f"Compilation failed. File {self.src_file_path} does not exist.")
        if not self.is_compiled:
            cal.make_ebpf_hike_program(self.src_file_path)
            self.is_compiled = True
        else:
            print(f"Hike program {self.program_name} is already compiled")

    def clean(self):
        os.remove(self.obj_file_path)
        os.remove(self.json_file_path)
        self.is_compiled = False

    def load(self):
        pinned_maps = {}

        map_dir = f"{settings.BPF_FS_MAPS_PATH}/{self.package}"
        cal.bpftool_prog_load(package=self.package, program_name=self.program_name,
                              pinned_maps=pinned_maps)

    def unload(self):
        raise NotImplemented("Unload not implemented")

    def register(self):
        key_values = ['{0:02x}'.format(self.program_id), '00', '00', '00']
        cal.bpftool_map_update(
            settings.PROGRAMS_REGISTER_MAP, key_values, self.program_path)

    def unregister(self):
        raise NotImplemented("Unregister not implemented")

    def write_map(self, map_name, key, data):
        pass

    def read_map(self, map_name, key):
        pass

    def get_maps(self):
        pass
