from cal import ebpf_system_init, hike_system_init
from chainloader import ChainLoader
from hikechain import HikeChain
from hikeprogram import HikeProgram
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
        ebpf_system_init()
        hike_system_init()

    def assign_id(self, element):
        # find an available id
        MIN_ID = 1
        MAX_ID = 255
        taken_id = [el['id']
                    for el in self.registered_ids]
        id = max(taken_id) + 1 if self.registered_ids else MIN_ID
        if id > MAX_ID:
            raise Exception("ID overflow")

        if isinstance(element, HikeChain):
            element_type = 'chain'
        elif isinstance(element, HikeProgram):
            element_type = 'program'
        else:
            raise Exception(f"Unknown element {element}")

        self.registered_ids.append({
            "type": element_type,
            "name": element.name,
            "package": element.package,
            "id": id})
        return id

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
            hc.link(self.registered_ids)
            hc.compile()
            hc.load()
            self.hike_chains[(hc.name, hc.package)] = hc

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
