from sly import Lexer, Parser


class IndentedLexer(Lexer):
    def preprocess(self, text):
        # convert tab in spaces
        text = text.replace('\t', '    ')
        # put INDENT and DEDENT
        INDENT = "_INDENT"
        DEDENT = "_DEDENT"
        curr_indentation_level = 0
        indentations = [0, ]
        output = ""

        for lineno, line in enumerate(lines):
            # remove spaces at the end and skip white lines
            line = line.rstrip()
            if not line:
                continue

            initial_spaces = len(line) - len(line.lstrip(' '))
            if initial_spaces > curr_indentation_level:
                indentations.append(initial_spaces)
                output += INDENT + line + '\n'
                #print("indenting of {} space".format(initial_spaces))
            elif initial_spaces < curr_indentation_level:
                indentations.pop()
                expected_spaces = indentations[-1]
                if expected_spaces != initial_spaces:
                    raise Exception("Syntax error on line {}: expected {} space for deindent ({} received)".format(
                        lineno, expected_spaces, initial_spaces))
                output += DEDENT + line + '\n'
            else:
                output += line + '\n'
            curr_indentation_level = initial_spaces
        # fill the remaining intendation
        while (len(indentations) > 1):
            indentation = indentations.pop()
            output += "DEDENT\n"

        return output

    def tokenize(self, text):
        return super().tokenize(self.preprocess(text))


class CalcLexer(Lexer):
    tokens = {ID, FROM, IMPORT}
    ignore = ' \t'
    literals = {'=', '+', '-', '*', '/', '(', ')', '.'}

    # Tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['from'] = FROM
    ID['import'] = IMPORT
    ID['pass'] = PASS

    NEWLINE = r'\n'
    COMMA = r','

    ignore_comment = r'[ ]*\043[^\n]*'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

    @_(r' [ ]+')
    def WS(self, t):
        return t

    @_(r' ')  # ignore single space
    def SS(self, t):
        pass


class EclatParser(Parser):
    tokens = EclatLexer.tokens

    precedence = (
    )

    def __init__(self):
        self.names = {}
        self.imports = []
        self.chains = {}

    @_('top_statements', '')
    def program(self, p):
        pass

    @_('top_statement top_statements')
    def top_statements(self, p):
        pass

    @_('top_statement')
    def top_statements(self, p):
        pass

    @_('import_stmt', 'void_stmt')
    def top_statement(self, p):
        pass

    @_('FROM ID IMPORT module_list NEWLINE')
    def import_stmt(self, p):
        # print(p)
        pass

    @_('ID COMMA module_list')
    def module_list(self, p):
        self.imports.append(p.ID)
        return p

    @_('ID')
    def module_list(self, p):
        self.imports.append(p.ID)
        return p

    @_('NEWLINE')
    def void_stmt(self, p):
        pass


if __name__ == '__main__':
    lexer = EclatLexer()
    parser = EclatParser()
    prog = \
        """
# test
from gino import mario
from pablo import andrea, stefano
from kilo import etto , grammo

def chain():
  # commento
  pass

"""
    tokens = lexer.tokenize(prog)
    for tok in tokens:
        print(tok)
    tokens = lexer.tokenize(prog)
    p = parser.parse(tokens)
    print(parser.imports)
    # while True:
    #    try:
    #        text = input('calc > ')
    #    except EOFError:
    #        break
    #    if text:
    #        print(lexer.tokenize(text))
    #        parser.parse(lexer.tokenize(text))
    #        # for tok in lexer.tokenize(text):
    #        #    print('type=%r, value=%r' % (tok.type, tok.value))
