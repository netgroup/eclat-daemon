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

    ignore_comment = r'\#.*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
    )

    def __init__(self):
        self.names = {}
        self.imports = []
        self.chains = {}

    @_('statement')
    def program(self, p):
        pass

    @_('import_stmt')
    def statement(self, p):
        pass

    @_('IMPORT ID')
    def import_stmt(self, p):
        print(p.ID)
        self.imports.append(p.ID)
        pass


if __name__ == '__main__':
    lexer = CalcLexer()
    parser = CalcParser()
    prog = \
        """
        # test
        import pippo
        import pluto
        """
    p = parser.parse(lexer.tokenize(prog))
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
