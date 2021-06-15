from parser.parser import getParser, getEnvironment
from parser.lexer import getLexer
from parser.utils import lexer_preprocessor
import settings
import cas
import os
import timeit

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

    # dest_folder is unsed and MAKE_FOLDER MAKE_FOLDER doesn't exist
    #def make_hike_chain(self, hike_source, dest_folder=settings.MAKE_FOLDER):
    def make_hike_chain(self, hike_source):
        """
        Make an hike chain.
        Call makefile on a hike C program, to create the object file.
        This object file can be loaded after in memory.

        The function returns the file path containing the compiled hike chain.
        """
        # 1. dump hike_source into a file
        hike_source_file = os.path.join(os.path.dirname(__file__), "runtime/output/eclat_output.hike.c")
        f = open(hike_source_file, "w")
        f.write(hike_source)
        f.close()
    
        # 2. call Makefile on top of that 
        makefile = os.path.join(os.path.dirname(__file__), settings.EXTERNAL_MAKEFILE_PATH)
        hike_dir = os.path.join(os.path.dirname(__file__), settings.HIKE_SOURCE_PATH)
        
        cas.make_hike_chain(makefile, hike_source_file, hike_dir)
        
        compiled_file = hike_source_file
        #hike_source_file[-1] = "o"     ERROR TypeError: 'str' object does not support item assignment
        compiled_file = compiled_file[:-1] + "o"

        return compiled_file


    def load_hike_chain(self, hike_compiled_file):
        """
        Load the compiled file into the memory
        """
        cas.hikecc(hike_compiled_file)


    def run(self, script):
        """
        Translate an ECLAT script into an HIKe Chain.
        Compile the chain and load it to memory.
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

        hike_source = self.translate_to_c(script)

        hike_compiled_file = self.make_hike_chain(hike_source)

        # self.load_hike_chain(hike_compiled_file)

        
        return True
