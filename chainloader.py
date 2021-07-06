class ChainLoader:
    def __init__(self, loader_name, package, configuration):
        pass

    def compile(self):
        pass

    def clean(self):
        pass

    def write_map(self, map_name, key, data):
        pass

    def read_map(self, map_name, key):
        pass

    def get_maps(self):
        pass

    def register(self):
        # Load all the classifiers
        # bpftool prog loadall classifier.o /sys/fs/bpf/progs/init type xdp \
        #	pinmaps /sys/fs/bpf/maps/init
        pass

    def unregister(self):
        pass
