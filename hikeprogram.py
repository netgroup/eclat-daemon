import settings
import os
import cal


class HikeProgram:
    program_id = None

    def __init__(self, package, program_name):
        self.program_name = program_name
        self.package = package
        self.is_compiled = False

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

    def compile(self):
        if not self.is_compiled:
            file_name = f"{self.package}.tar.gz"
            file_path = f"{settings.PROGRAMS_DIR}/{self.package}/{file_name}.ebpf.c"
            cal.make_ebpf_hike_program(file_path)
            self.is_compiled = True

    def clean(self):
        pass

    def load(self):
        pass

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
