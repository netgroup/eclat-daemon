from .eclat_ast import *
from sly import Lexer, Parser
import re
from .lexer import EclatLexer


class EclatParser(Parser):
    tokens = EclatLexer.tokens
    debugfile = 'parser.out'

    precedence = (
        ('left', 'COLON'),
        ('left', 'ASSIGN'),
        #('left', ['[', ']', ',']),
        ('left', 'IF', 'ELIF', 'NEWLINE', 'END'),
        # ('left', ['IF', 'ELSE', 'END',
        #          'NEWLINE', 'WHILE', ]),
        #('left', 'AND', 'OR', ),
        #('left', 'NOT', ),
        ('left', 'EQ', 'NEQ', 'GTE', 'GT', 'LT', 'LTE', ),
        #('left', ['PIPE', ]),
        #('left', ['^', ]),
        #('left', ['&', ]),
        #('left', ['>>', '<<', ]),
        ('left', 'PLUS', 'MINUS', ),
        ('left', 'MULT', 'DIV', ),

        # REFERENCE
        #('left', 'PLUS', 'MINUS'),
        #('left', 'LTE', 'GTE', 'GT', 'LT',),
        #('left', 'EQ'),
        #('left', 'ASSIGN'),
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

    @_('statement_full', 'statement_full program')
    def program(self, p):
        pass

    @_('statement NEWLINE', 'statement')
    def statement_full(self, p):
        return p.statement

    @_('chain_statement', 'import_statement')
    def statement(self, p):
        return p

    @_('FROM NAME IMPORT module_list')
    def import_statement(self, p):
        self.imports[p.NAME] = self._imports_name[:]
        self._imports_name = []

    @ _('NAME COMMA module_list',
        'NAME')
    def module_list(self, p):
        self._imports_name.append(p.NAME)
        return p

    @_('DEF NAME LPAR arglist RPAR COLON NEWLINE block')
    def chain_statement(self, p):
        c = Chain(p.NAME, p.arglist, p.block)
        print(f"Printing {p.NAME} code:\n")
        print("------------------------------")
        print(c.to_c())
        print("------------------------------")
        if p.NAME in self.chains.keys():
            raise Exception(f"Chain {p.NAME} has already been defined")
        self.chains[p.NAME] = c

    @_('INDENT block_statements DEDENT')
    def block(self, p):
        b = Block(self.statement_list[:])
        self.statement_list = []
        return b

    @_('statement_full', 'statement_full block_statements')
    def block_statements(self, p):
        self.statement_list.insert(0, p.statement_full)
        return self.statement_list

    # statements
    @_('PASS')
    def statement(self, p):
        return Pass()

    @_('expression')
    def statement(self, p):
        return Statement(p.expression)

    @_('ELIF expression COLON NEWLINE block',)
    def elif_statement(self, p):
        return Elif(p.expression, p.block)

    @_('IF expression COLON NEWLINE block NEWLINE elif_statement',
       'IF expression COLON NEWLINE block NEWLINE')
    def statement(self, p):
        elif_part = getattr(p, 'elif_statement', None)
        else_part = getattr(p, 'else_statement', None)
        return If(p.expression, p.block, elif_part, else_part)

    # expressions
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
        return BinaryExpression(p.expression0, p[1], p.expression1)

    @ _('NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME))

    @ _('const')
    def argument(self, p):
        self.argument_list.append(Argument(p.const))

    @ _('argument COMMA arglist', 'argument', '')
    def arglist(self, p):
        return self.argument_list

    @ _('type COLON NAME')
    def argument(self, p):
        self.argument_list.append(Argument(p.NAME, p.type))

    @_('const', 'NAME')
    def expression(self, p):
        return Expression(p[0])

    @_('NAME ASSIGN expression')
    def statement(self, p):
        return Assigment(p.NAME, p.expression)

    @_('type COLON NAME ASSIGN const')
    def statement(self, p):
        return Assigment(p.NAME, p.const, p.type)

    @_('type COLON NAME ASSIGN expression')
    def statement(self, p):
        return Assigment(p.NAME, p.expression, p.type)

    @ _('U8', 'U16', 'U32', 'U64', 'S8', 'S16', 'S32', 'S64')
    def type(self, p):
        return Type(p[0])

    @_('HEX', 'FLOAT', 'INTEGER', 'STRING', 'BOOLEAN')
    def const(self, p):
        return p[0]

    def error(self, p):
        raise SyntaxError(
            f"Syntax error at token {p.type} on line {p.lineno}, index {p.index} and value {p.value}")
