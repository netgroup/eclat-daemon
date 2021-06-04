from parser.parser import getParser, getEnvironment
from parser.lexer import getLexer
from parser.utils import lexer_preprocessor

from Interface_i1.interface_i1 import *

import os

class EclatEngine:
    def __init__(self):
        self.lexer, syntax_tokens = getLexer()
        self.parser = getParser(syntax_tokens)  # pg.build()
        self.env = getEnvironment()

    def translate_to_c(self, script):
        """
        Translate the script from Eclat to C
        Generate the Hyke program
        """
        print(f"Translating script: \n{script}")

        preprocessed_script = lexer_preprocessor(script)
        tokens = self.lexer.lex(preprocessed_script)

        program = self.parser.parse(tokens)

        code = program.exec(self.env)
        print(f"Translated to: \n{code}")

        return code

    def run(self, script):
        """
        Compile the Hyke program
        """
        # Ogni volta che viene eseguita la traduzione viene
        # riscritto/aggiornato il file "registry.csv" che si trova 
        # all'interno della cartella "runtime". In questo file 
        # vengono memorizzate tutte le chain "caricate" tramite eCLAT, 
        # con associato: 
        # - ID progressivo delle chain;
        # - il nome del modulo;
        # - nome della chain.
        # NOTA: Se presenti due chain con lo stesso nome all'interno
        #       dello stesso modulo genera un errore visto che devono
        #       essere univoche. 

        hyke_program = self.translate_to_c(script)
        
        # se serve scrivere output su file
        f = open("/opt/eclat-daemon/runtime/output/eclat_output.hike.c", "w")
        f.write(hyke_program)
        f.close()

        
        # MOUNT
        # os.system(mount("/sys/fs/bpf/", "bpf"))
        # os.system(mount("/sys/kernel/tracing", "tracefs"))

        # os.system(mkdir("/sys/fs/bpf/progs"))
        # os.system(mkdir("/sys/fs/bpf/maps"))

        # TODO make
        MAKEFILE_PATH = "/opt/hike_v3/external/Makefile"
        HIKE_DIR_PATH = "/opt/hike_v3/src/"

        # Il build viene generato in "output"
        os.chdir('/opt/eclat-daemon/runtime/output')
        os.system(make(MAKEFILE_PATH, "chain", "eclat_output", HIKE_DIR_PATH))

        # TODO load
        OBJ_PATH = HIKE_DIR_PATH + "/build/eclat_output.hike.o"
        MAP_PATH = "/sys/fs/bpf/maps/hike_chain_map"
        OUTPUT_PATH = "/opt/eclat-daemon/runtime/output"

        os.system(hikecc(OBJ_PATH, MAP_PATH, OUTPUT_PATH))


        return True
