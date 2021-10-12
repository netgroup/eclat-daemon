class HikeChain:
    """[summary]
    """
    chain_id = None

    # def pull(self):
    #     # needed?
    #     # better another constructor
    #     pass
    def __init__(self, name, code, programs_map, globals):
        self.name = name
        self.code = code
        self.programs_map = programs_map
        self.globals = globals

    def compile(self):
        # take code and add macros for the maps
        # add the globals
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
