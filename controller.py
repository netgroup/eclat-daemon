from cal import ebpf_system_init, hike_system_init
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
        tokens = EclatLexer().tokenize(eclat_script)
        parser = EclatParser()
        parser.parse(tokens)
        print(parser.imports)
        print(parser.chains)

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
