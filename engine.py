from parser.parser import getParser, getEnvironment
from parser.lexer import getLexer
from parser.utils import lexer_preprocessor


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
        hyke_program = self.translate_to_c(script)
        # f = open("eclat_output.c", "w")
        # f.write(output)
        # f.close()

        # TBD make
        # TBD load
        return True
