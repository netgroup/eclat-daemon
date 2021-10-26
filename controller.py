from cal import ebpf_system_init, hike_system_init
from chainloader import ChainLoader
from hikechain import HikeChain
from hikeprogram import HikeProgram
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class EclatController:
    hike_programs = {}
    hike_chains = {}
    chain_loaders = {}
    registered_ids = []  # {type, package, name, id}

    def __init__(self):
        ebpf_system_init()
        hike_system_init()

    # def load_hike_program(self):
    #     PROG_NAME = 'testprog'
    #     PROG_PKG = 'testpkg'
    #     if 'testprog' not in self.hike_programs.keys():
    #         self.hike_programs['test'] = HikeProgram(PROG_NAME, PROG_PKG)
    #     p = self.hike_programs['test']
    #     p.pull()
    def assign_id(self, element):
        # find an available id
        MIN_ID = 0
        MAX_ID = 255
        taken_id = [el['id'] for el in self.registered_ids]
        id = max(taken_id) + 1
        if id > MAX_ID:
            raise Exception("ID overflow")

        if element is HikeChain:
            element_type = 'chain'
        elif element is HikeProgram:
            element_type = 'program'

        self.registered_ids.append({
            "type": element_type,
            "name": element.name,
            "package": element.package,
            "id": id})
        return id

    def load_configuration(self, eclat_script):
        # Parse the config
        tokens = EclatLexer().tokenize(eclat_script)
        parser = EclatParser()
        parser.parse(tokens)
        print(parser.imports)
        print(parser.chains)

        # set up hike programs
        for package, names in parser.imports['programs'].items():
            for name in names:
                if not (name, package) in self.hike_programs.keys():
                    hp = HikeProgram(name, package)
                    hp.pull()
                    hp.compile()
                    hp.load()
                    p_id = self.assign_id(hp)
                    hp.register(p_id)
                    self.hike_programs[(hp.name, hp.package)] = hp

        # pre-register chain ids
        chains = []
        for chain_name, ast_chain in parser.chains.items():
            # get the package name
            chain_package = None
            for package, names in parser.imports['programs'].items():
                if chain_name in names:
                    chain_package = package

            hc = HikeChain(
                name=ast_chain.name, package=chain_package, code=ast_chain.to_c(), globals=parser.globals)
            c_id = self.assign_id(hc)
            chains.append((hc, c_id))

        # set up chains
        for chain, chain_id in chains:
            hc.link(self.registered_ids)
            hc.compile()
            hc.load()
            self.hike_chains[(hc.name, hc.package)] = hc

        # set up chain loaders
        for loader in parser.loaders:
            # get the package
            loader_package = None
            for package, name in parser.imports['loaders']:
                if name == loader['name']:
                    loader_package = package

            hl = ChainLoader(name, package)
            hl.compile()
            hl.load()

            dev = loader['dev']
            attach_type = loader['attach_type']
            hl.attach(dev, attach_type)
            hl.write_map('todo', [1, 2, 3], [4, 5, 6])
            self.chain_loaders[(hl.name, hl.package)] = hl
