from sly import Lexer, Parser


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
