from parser.parser import getParser
from parser.lexer import getLexer
from parser.utils import lexer_preprocessor


class EclatEngine:
    def __init__(self):
        self.lexer, syntax_tokens = getLexer()
        self.parser = getParser(syntax_tokens)  # pg.build()

    def run(self, script):
        # 1 parsing script
        preprocessed_script = lexer_preprocessor(script)
        tokens = self.lexer.lex(preprocessed_script)

        print(list(tokens))

        program = self.parser.parse(tokens)

        # 2 script execution
        program.exec()

        print(f"Running {script}")
        return True
