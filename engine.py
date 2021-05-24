from parser.parser import getParser
from parser.lexer import getLexer
from parser.utils import indent_script


class EclatEngine:
    def __init__(self):
        self.lexer = getLexer()
        self.parser = getParser()  # pg.build()

    def run(self, script):
        # 1 parsing script
        indented_script = indent_script(script)
        tokens = self.lexer.lex(indented_script)
        program = self.parser.parse(tokens)

        # 2 script execution
        program.exec()

        print(f"Running {script}")
        return True
