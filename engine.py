from parser.parser import getParser
from parser.lexer import getLexer
from parser.utils import indent_script


class EclatEngine:
    def __init__(self):
        self.lexer = getLexer()
        self.parser = getParser()  # pg.build()

    def run(self, script):
        # 1 parsing script
        intented_script = indent_script(script)
        tokens = self.lexer.lex(indented_script)
        program = self.parser.parse(tokens)

        # 2 script execution
        program.exec()

        print(f"Running {script}")
        return True


fname = args
  # prende il nome del package
  package_name = fname.split("/")[-1].split(".")[0]
   with open(fname) as f:
        text_input = f.read()
    lexer = 
    tokens = detect_indent(lexer, text_input)
    # for i in tokens:
    #    print(i)

    parser.parse(tokens).exec(Environment())
