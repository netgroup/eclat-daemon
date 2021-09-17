from .eclat_ast import *
from sly import Lexer, Parser
import re
from .lexer import EclatLexer


class EclatParser(Parser):
    tokens = EclatLexer.tokens

    precedence = (
    )

    def __init__(self):

        self.imports = {}
        self.chains = {}
        self.loaders = {}
        # stack for the parser
        self.statement_list = []
        self.argument_list = []

        #####
        self._imports_name = []

    @_('top_statements')
    def program(self, p):
        pass

    @_('top_statement top_statements',
       'top_statement')
    def top_statements(self, p):
        pass

    @_('import_stmt NEWLINE', 'chain_stmt NEWLINE')
    def top_statement(self, p):
        pass

    @_('DEF NAME LPAR arglist RPAR COLON NEWLINE block')
    def chain_stmt(self, p):
        c = Chain(p.NAME, p.block)
        print("Printing {} code:\n".format(p.NAME))
        print(c.to_c())
        if p.NAME in self.chains.keys():
            raise Exception(f"Chain {p.NAME} has already been defined")
        self.chains[p.NAME] = c

    @_('INDENT statements DEDENT')
    def block(self, p):
        b = Block(self.statement_list)
        self.statement_list = []
        return b

    @_('statement NEWLINE statements', 'statement NEWLINE')
    def statements(self, p):
        self.statement_list.append(p.statement)
        return self.statement_list

    @_('PASS')
    def statement(self, p):
        return Pass()

    @_('NAME LPAR arglist RPAR', 'NAME LPAR RPAR')
    def statement(self, p):
        return Pass()

    @_('HEX', 'FLOAT', 'INTEGER', 'STRING', 'BOOLEAN')
    def const(self, p):
        return p[0]

    @_('NAME ASSIGN const')
    def statement(self, p):
        return Assigment(p.NAME, p.const)

    @_('type COLON NAME ASSIGN const')
    def statement(self, p):
        return Assigment(p.NAME, p.const, p.type)

    @_('')
    def argument(self, p):
        pass

    @_('NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME))

    @_('argument COMMA arglist', 'argument', '')
    def arglist(self, p):
        pass

    @_('type COLON NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME, p.type))

    @_('U8', 'U16', 'U32', 'U64', 'S8', 'S16', 'S32', 'S64')
    def type(self, p):
        return Type(p[0])

    @_('FROM NAME IMPORT module_list')
    def import_stmt(self, p):
        self.imports[p.NAME] = self._imports_name
        self._imports_name = []

    @_('NAME COMMA module_list',
       'NAME')
    def module_list(self, p):
        self._imports_name.append(p.NAME)
        return p

    ########### TODO #########
    # expression
    # statements: if, while, for, return

    # chiamare i moduli
    # modificare mappe (?)

    # const
    # variabili globali


# if __name__ == '__main__':
#     lexer = EclatLexer()
#     parser = EclatParser()
#     prog = """
# # test
# from gino import mario
# from pablo import andrea, stefano, pino
# from kilo import etto , grammo

# from package1 import p1

# def chain1():
#   a = 2
#   pass

# def chain2():
#     u8 : b = 7

# """
#     tokens = lexer.tokenize(prog)
#     for tok in tokens:
#         print(tok)
#     tokens = lexer.tokenize(prog)
#     p = parser.parse(tokens)
#     print(parser.imports)
#     print(parser.chains)
#     # while True:
#     #    try:
#     #        text = input('calc > ')
#     #    except EOFError:
#     #        break
#     #    if text:
#     #        print(lexer.tokenize(text))
#     #        parser.parse(lexer.tokenize(text))
#     #        # for tok in lexer.tokenize(text):
#     #        #    print('type=%r, value=%r' % (tok.type, tok.value))
