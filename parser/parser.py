from .eclat_ast import *
from sly import Lexer, Parser
import re
from .lexer import EclatLexer


class EclatParser(Parser):
    tokens = EclatLexer.tokens

    precedence = (
        #    ('left', 'PLUS', 'MINUS'),
        #
        #    ('left', 'LTE', 'GTE', 'GT', 'LT',),
        #    ('left', 'EQ'),
        #    ('left', 'ASSIGN'),
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
        c = Chain(p.NAME, p.arglist, p.block)
        print(f"Printing {p.NAME} code:\n")
        print("------------------------------")
        print(c.to_c())
        print("------------------------------")
        if p.NAME in self.chains.keys():
            raise Exception(f"Chain {p.NAME} has already been defined")
        self.chains[p.NAME] = c

    @_('INDENT statements DEDENT')
    def block(self, p):
        b = Block(self.statement_list[:])
        self.statement_list = []
        return b

    @_('statement NEWLINE statements', 'statement NEWLINE')
    def statements(self, p):
        self.statement_list.insert(0, p.statement)
        return self.statement_list

    @_('PASS')
    def statement(self, p):
        return Pass()

    @_('NAME LPAR arglist RPAR')
    def expression(self, p):
        # function call
        argument_list = self.argument_list[:]
        self.argument_list = []
        return FunctionCall(p.NAME, argument_list)

    @_('expression PLUS expression',
        'expression MINUS expression',
        'expression MULT expression',
        'expression DIV expression',
        'expression GTE expression',
        'expression LTE expression',
        'expression GT expression',
        'expression LT expression',
        'expression EQ expression'
       )
    def expression(self, p):
        print(p)
        return BinaryExpression(p.expression0, p[1], p.expression1)

    @_('expression')
    def statement(self, p):
        return Statement(p.expression)

    @_('HEX', 'FLOAT', 'INTEGER', 'STRING', 'BOOLEAN')
    def const(self, p):
        return p[0]

    @_('const')
    def expression(self, p):
        return p[0]

    @_('NAME ASSIGN expression')
    def statement(self, p):
        print("XXXXXXXXXX")
        return Assigment(p.NAME, p.expression)

    # @_('NAME ASSIGN const')
    # def statement(self, p):
    #    print("XXXX")
    #    return Assigment(p.NAME, p.const)

    @_('type COLON NAME ASSIGN const')
    def statement(self, p):
        return Assigment(p.NAME, p.const, p.type)

    @_('type COLON NAME ASSIGN expression')
    def statement(self, p):
        return Assigment(p.NAME, p.expression, p.type)

    @_('IF expression COLON NEWLINE block')
    def statement(self, p):
        return If(p.expression, p.block)

    @_('NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME))

    @_('const')
    def argument(self, p):
        self.argument_list.append(Argument(p.const))

    @_('argument COMMA arglist', 'argument', '')
    def arglist(self, p):
        #argument_list = self.argument_list[:]
        print(f"In arglist - length = {len(self.argument_list)}")
        #self.argument_list = []
        # return argument_list
        return self.argument_list

    @_('type COLON NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME, p.type))

    @_('U8', 'U16', 'U32', 'U64', 'S8', 'S16', 'S32', 'S64')
    def type(self, p):
        return Type(p[0])

    @_('FROM NAME IMPORT module_list')
    def import_stmt(self, p):
        self.imports[p.NAME] = self._imports_name[:]
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
