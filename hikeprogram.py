import settings
import os
import cal


class HikeProgram:
    program_id = None

    def __init__(self, package, program_name):
        self.program_name = program_name
        self.package = package
        ###
        self.src_file_path = f"{settings.PROGRAMS_DIR}/{self.package}/{program_name}.bpf.c"
        self.obj_file_path = f"{settings.BUILD_PROGRAMS_DIR}/{self.package}/{program_name}.bpf.o"
        self.json_file_path = f"{settings.BUILD_PROGRAMS_DIR}/{self.package}/{program_name}.bpf.json"
        self.is_compiled = self._is_compiled()

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
            #file_name = f"{self.package}.tar.gz"

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
        program_path = f"{settings.BPF_FS_PROGS_PATH}/{self.package}/{self.program_name}"
        map_dir = f"{settings.BPF_FS_MAPS_PATH}/{self.package}"
        cal.bpftool_prog_load(program_object=self.obj_file_path, program_fs_path=program_path,
                              pinned_maps=pinned_maps, program_maps_fs_path=map_dir)

    def unload(self):
        pass

    def register(self):
        pass

    def unregister(self):
        pass

    def write_map(self, map_name, key, data):
        pass

    def read_map(self, map_name, key):
        pass

    def get_maps(self):
        pass
