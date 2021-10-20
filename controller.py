from cal import ebpf_system_init, hike_system_init
from hikechain import HikeChain
from hikeprogram import HikeProgram
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class EclatController:
    hike_programs = {}
    hike_chain = {}
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

        # load hike programs
        for names, package in parser.imports:
            for name in names:
                if not (name, package) in self.hike_programs.keys():
                    hp = HikeProgram(name, package)
                    hp.pull()
                    hp.compile()
                    hp.load()
                    p_id = self.assign_id(hp)
                    hp.register(p_id)
                    self.hike_programs[(name, package)] = hp

        # pre-register chain ids
        chains = []
        for ast_chain in parser.chains:

            hc = HikeChain(
                name=ast_chain.name, code=ast_chain.to_c(), globals=parser.globals)
            c_id = self.assign_id(hc)
            chains.append((hc, c_id))
        for chain, chain_id in chains:
            hc.link(self.registered_ids)
            hc.compile()
            hc.load()
            self.hike_chain[ast_chain.name] = hc
        # update program_id with the id of the new created chain
        # alla chain

        # TODO load chainloader

        #

        #data = prog.eval()
        # 1. genera una struttura dati
        # il parser capisce solo la sintassi, non esegue comandi
        # struttura dati (con dei SIMBOLI al prosto degli id):
        # --programs: [LIST OF NAMES],
        # --chains: {chain_name: c_code},
        # --loader: {name: ‘xdd’, ‘configuration: {...}’}

        # 2. linking
        # self.import_programs(data.programs)
        # self.link(data)

        # #############################################
        # deps = prog.get_dependencies()
        # id_maps = self.resolve_dependencies()
        # # ritorna lista di programmi, mappe, e chain
        # prog.eval(id_maps)
        # # --programs: [LIST OF NAMES],
        # # --chains: {chain_name: c_code},
        # # --loader: {name: ‘xdd’, ‘configuration: {...}’}

        # ############################################
        # ImportBlock .eval()
        # .to_c()

        # IfBlock
        # .eval()  # che fa?
        # .to_c()
