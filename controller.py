from cal import ebpf_system_init, hike_system_init
from hikechain import HikeChain
from hikeprogram import HikeProgram
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class EclatController:
    hike_programs = {}
    hike_chain = {}

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

    def load_configuration(self, eclat_script):
        # Parse the config
        tokens = EclatLexer().tokenize(eclat_script)
        parser = EclatParser()
        parser.parse(tokens)
        print(parser.imports)
        print(parser.chains)

        # load hikeprograms
        for package, functions in parser.imports:
            for function in functions:
                if not (package, function) in self.hike_programs.keys():
                    hp = HikeProgram(package, function)
                    hp.pull()
                    hp.compile()
                    hp.load()
                    hp.register()
                    self.hike_programs[(package, function)] = hp

        programs_map = [f + (hp.program_id,)
                        for f, hp in self.hike_programs.items()]
        for ast_chain in parser.chains:
            self.hike_chain[ast_chain.name] = HikeChain(
                name=ast_chain.name, code=ast_chain.to_c(), programs_map=programs_map, globals=parser.globals)

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
