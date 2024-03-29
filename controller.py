import cal
from chainloader import ChainLoader
from hikechain import HikeChain
from hikeprogram import HikeProgram
from package_manager import PackageManager
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class EclatController:
    """Controller is the Eclat main class. 
    It is responsible of keeping the state and interpret high level commands
    such as load configuration which interprets an eclat script and apply it.
    """
    hike_programs = {}
    hike_chains = {}
    chain_loaders = {}
    registered_ids = []  # {type, package, name, id}

    def __init__(self):
        cal.ebpf_system_init()
        cal.hike_system_init()

    def assign_id(self, element):
        # find an available id
        MIN_CHAIN_ID = 1073741824+1
        # MIN_CHAIN_ID = 1073741824+86
        MAX_CHAIN_ID = 1073741824+255
        MIN_PROGRAM_ID = 1
        MAX_PROGRAM_ID = 255
        # MIN_CHAIN_ID = 64
        # MAX_CHAIN_ID = 255
        # MIN_PROGRAM_ID = 1
        # MAX_PROGRAM_ID = 63

        if isinstance(element, HikeChain):
            chain_taken_id = [el['id']
                              for el in self.registered_ids if el['type'] == 'chain']
            id = max(chain_taken_id) + \
                1 if (self.registered_ids and chain_taken_id) else MIN_CHAIN_ID
            if id > MAX_CHAIN_ID:
                raise Exception("ID overflow")
            element_type = 'chain'
        elif isinstance(element, HikeProgram):
            program_taken_id = [el['id']
                                for el in self.registered_ids if el['type'] == 'program']
            id = max(program_taken_id) + \
                1 if (self.registered_ids and program_taken_id) else MIN_PROGRAM_ID
            if id > MAX_PROGRAM_ID:
                raise Exception("ID overflow")
            element_type = 'program'
        else:
            raise Exception(f"Unknown element {element}")

        self.registered_ids.append({
            "type": element_type,
            "name": element.name,
            "package": element.package,
            "id": id})
        return id

    def fetch_configuration(self, eclat_script):
        """
        Download the packages requested by an eclat script (without loading anything).
        """
        pm = PackageManager()
        # Parse the config
        tokens = EclatLexer().tokenize(eclat_script)
        parser = EclatParser()
        parser.parse(tokens)

        # set up hike programs
        for package, names in parser.imports['programs'].items():
            for name in names:
                if package != 'hike':  # reserved for system programs
                    pm.pull(package)

        # set up chain loaders
        for package, names in parser.imports['loaders'].items():
            pm.pull(package)
        return True

    def fetch_package(self, package):
        """Download all the packages requested by the script
        """
        pm = PackageManager()
        return pm.pull(package)

    def load_configuration(self, eclat_script, script_package):
        # Parse the config
        tokens = EclatLexer().tokenize(eclat_script)
        parser = EclatParser()
        parser.parse(tokens)

        # set up hike programs
        for package, names in parser.imports['programs'].items():
            for name in names:
                # if not already running, launch the hike programs
                if not (name, package) in self.hike_programs.keys():
                    if package != 'hike':  # reserved for system programs
                        hp = HikeProgram(name, package)
                        hp.pull()
                        hp.compile()
                        hp.load()
                        p_id = self.assign_id(hp)
                        hp.register(p_id)
                        self.hike_programs[(hp.name, hp.package)] = hp
                else:
                    print((name, package), ' is ALREADY RUNNING')

        # pre-register chains ids
        chains = []
        for chain_name, ast_chain in parser.chains.items():
            chain_package = script_package  # get the package name
            hc = HikeChain(
                name=ast_chain.name, package=chain_package, code=ast_chain.to_c(chain_package), globals=parser.globals)
            c_id = self.assign_id(hc)
            chains.append((hc, c_id))

        # set up chains
        for chain, chain_id in chains:
            chain.link(self.registered_ids)
            chain.compile()
            chain.load()
            self.hike_chains[(chain.name, chain.package)] = hc

        # set up chain loaders
        for package, names in parser.imports['loaders'].items():
            assert(len(names) == 1)  # currently we support just one loader
            name = names[0]
            # get loader configuration information
            loader_info = None
            for li in parser.loaders:
                if li['name'] == name and li['package'] == package:
                    loader_info = li
            assert(loader_info)  # we need one loader configuration

            attach_type, dev = loader_info['attach_type'], loader_info['dev']

            hl = ChainLoader(name, package)
            hl.pull()
            hl.compile()
            hl.load()
            parser.maps = hl.link(parser.maps, self.registered_ids)
            hl.attach(dev, attach_type)

            # configure maps for loaders
            for map_configuration in filter(lambda x: x['program_name'] == name, parser.maps):
                for key, value in map_configuration['data'].items():
                    hl.write_map(map_configuration['map_name'], key, value)
            self.chain_loaders[(hl.name, hl.package)] = hl
        return True

    def get_map_value(self, mapname, key):
        """
        Returns the value corresponding to a given key in a specific map
        """
        return cal.bpftool_map_lookup(mapname, int(key))

    def dump_map(self, mapname):
        """
        Dumps the content of a specific map
        """
        return cal.bpftool_map_dump(mapname)
