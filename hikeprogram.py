class HikeProgram:
    program_id = None

    def __init__(self, program_name, package, configuration):
        self.program_name = program_name
        self.package = package
        self.configuration = configuration
        pass

    def download(self):
        # pip install --install-option="--prefix=$PREFIX_PATH" package_name
        pass

    def compile(self):
        pass

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
