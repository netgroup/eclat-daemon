from .eclat_ast import *
from sly import Lexer, Parser
import re
import json
from .lexer import EclatLexer


class EclatParser(Parser):
    tokens = EclatLexer.tokens
    #debugfile = 'parser.out'

    precedence = (
        ('left', 'COLON'),
        ('left', 'ASSIGN'),
        # ('left', ['[', ']', ',']),
        ('left', 'IF', 'ELIF', 'NEWLINE', 'END'),
        # ('left', ['IF', 'ELSE', 'END',
        #          'NEWLINE', 'WHILE', ]),
        # ('left', 'AND', 'OR', ),
        # ('left', 'NOT', ),
        ('left', 'EQ', 'NEQ', 'GTE', 'GT', 'LT', 'LTE', ),
        # ('left', ['PIPE', ]),
        # ('left', ['^', ]),
        # ('left', ['&', ]),
        # ('left', ['>>', '<<', ]),
        ('left', 'PLUS', 'MINUS', ),
        ('left', 'MULT', 'DIV', ),

        # REFERENCE
        # ('left', 'PLUS', 'MINUS'),
        # ('left', 'LTE', 'GTE', 'GT', 'LT',),
        # ('left', 'EQ'),
        # ('left', 'ASSIGN'),
    )

    def __init__(self):

        self.imports = {'programs': {}, 'loaders': {}}  # import set
        self.chains = {}  # chains code
        self.loaders = []  # chain loader configuration
        self.globals = []  # global variables
        #  configure maps - {'program_name': ..., 'map_name': ..., 'data' {k1: v1, k2: v2}}
        self.maps = []
        # function mapper
        self.mapper = {}  # eye candy for "objects"

    @_('statement_full', 'statement_full program')
    def program(self, p):
        if p.statement_full:
            # only global statements return
            self.globals.append(p.statement_full.to_c())
        return {'imports': self.imports,
                'chains': self.chains,
                'loaders': self.loaders,
                'globals': self.globals
                }

    @_('statement NEWLINE', 'statement')
    def statement_full(self, p):
        return p.statement

    @_('chain_statement', 'import_statement', 'map_statement')
    def statement(self, p):
        # top statements
        return p[0]

    @_('FROM NAME DOT NAME IMPORT module_list')
    def import_statement(self, p):
        if not p.NAME0 in ['programs', 'loaders']:
            raise Exception(
                "Bad import statement: from {programs|loaders}.package import name")
        self.imports[p.NAME0][p.NAME1] = p.module_list
        if p.NAME1 == 'hike':
            with open('parser/mapper/hike.json') as f:
                d = json.load(f)
                self.mapper.update(d)

    @ _('NAME COMMA module_list',
        'NAME')
    def module_list(self, p):
        if hasattr(p, "module_list"):
            return [p.NAME, ] + p.module_list
        else:
            return [p.NAME, ]

    @_('NAME LSPAR NAME RSPAR ASSIGN kv_mapping')
    def map_statement(self, p):
        print(f"Map {p.NAME1} configuration: ", p.kv_mapping.to_python())
        self.maps.append({
            'program_name': p.NAME0,
            'map_name': p.NAME1,
            'data': p.kv_mapping.to_python()
        })

    @_('LCPAR key_value_pairs RCPAR', 'LCPAR NEWLINE INDENT key_value_pairs DEDENT NEWLINE RCPAR')
    def kv_mapping(self, p):
        d = Dictionary(p.key_value_pairs)
        return d

    @_('key_value_pair COMMA key_value_pairs',
       'key_value_pair COMMA NEWLINE key_value_pairs',
       'key_value_pair NEWLINE',
       'key_value_pair', '')
    def key_value_pairs(self, p):
        if hasattr(p, 'key_value_pairs'):
            return [p.key_value_pair, ] + p.key_value_pairs
        else:
            return [p.key_value_pair, ]

    @_('LPAR exprlist RPAR COLON LPAR exprlist RPAR')
    def key_value_pair(self, p):
        return p.exprlist0, p.exprlist1

    @_('DEF NAME LPAR arglist RPAR COLON NEWLINE block')
    def chain_statement(self, p):
        c = Chain(p.NAME, p.arglist, p.block)
        print(f"Printing {p.NAME} code:\n")
        print("------------------------------")
        print(c.to_c('testing_package'))
        print("------------------------------")
        if p.NAME in self.chains.keys():
            raise Exception(f"Chain {p.NAME} has already been defined")
        self.chains[p.NAME] = c

    @_('INDENT block_statements DEDENT')
    def block(self, p):
        b = Block(p.block_statements)
        return b

    @_('statement_full', 'statement_full block_statements')
    def block_statements(self, p):
        if hasattr(p, "block_statements"):
            return [p.statement_full, ] + p.block_statements
        else:
            return [p.statement_full, ]

    # statements
    @_('PASS')
    def statement(self, p):
        return Pass()

    @_('expression')
    def statement(self, p):
        return Statement(p.expression)

    @_('ELSE COLON NEWLINE block',)
    def else_statement(self, p):
        return Else(p.block)

    @_('ELIF expression COLON NEWLINE block NEWLINE elif_statement',
       'ELIF expression COLON NEWLINE block NEWLINE else_statement',
       'ELIF expression COLON NEWLINE block NEWLINE')
    def elif_statement(self, p):
        elif_part = getattr(p, 'elif_statement', None)
        else_part = getattr(p, 'else_statement', None)
        return Elif(p.expression, p.block, elif_part, else_part)

    @_('IF expression COLON NEWLINE block NEWLINE elif_statement',
        'IF expression COLON NEWLINE block NEWLINE else_statement',
       'IF expression COLON NEWLINE block NEWLINE')
    def statement(self, p):
        elif_part = getattr(p, 'elif_statement', None)
        else_part = getattr(p, 'else_statement', None)
        return If(p.expression, p.block, elif_part, else_part)

    @_('WHILE expression COLON NEWLINE block')
    def statement(self, p):
        return While(p.expression, p.block)

    # @_('FOR expression COLON NEWLINE block')
    # def statement(self, p):
    #    return For(p.expression, p.block)

    @_('RETURN expression', 'RETURN')
    def statement(self, p):
        if hasattr(p, 'expression'):
            return Return(p.expression)
        else:
            return Return(Expression(0))

    # expressions
    @_('NAME LPAR exprlist RPAR', 'NAME DOT NAME LPAR exprlist RPAR')
    def expression(self, p):
        # function call
        expression_list = p.exprlist
        if hasattr(p, 'NAME1'):
            # method call
            print(f"method call {p.NAME0}.{p.NAME1}: {expression_list}")
            return FunctionCall(p.NAME1, expression_list, globals=self.globals, object=p.NAME0, imports=self.imports, mapper=self.mapper, loaders=self.loaders)
        else:
            # function call
            return FunctionCall(p.NAME, expression_list, globals=self.globals, imports=self.imports, mapper=self.mapper, )

    @_('expression PLUS expression',
        'expression MINUS expression',
        'expression MULT expression',
        'expression DIV expression',
        'expression MOD expression',
        'expression GTE expression',
        'expression LTE expression',
        'expression GT expression',
        'expression LT expression',
        'expression EQ expression',
        'expression NEQ expression',
        'expression AND expression',
        'expression OR expression',
       )
    def expression(self, p):
        return BinaryExpression(p.expression0, p[1], p.expression1)

    @_('NOT expression')
    def expression(self, p):
        return UnaryExpression(p[0], p.expression)

    @_('LPAR expression RPAR')
    def expression(self, p):
        exp = p.expression
        exp.set_brackets()
        return exp

    @ _('argument COMMA arglist', 'argument', '')
    def arglist(self, p):
        if hasattr(p, "arglist"):
            return [p.argument, ] + p.arglist
        elif hasattr(p, "argument"):
            return [p.argument, ]
        else:
            return []

    @ _('type COLON NAME')
    def argument(self, p):
        return Argument(p.NAME, p.type)

    @ _('const', 'NAME')
    def expression(self, p):
        return Expression(p[0])

    @ _('expression COMMA exprlist', 'expression', '')
    def exprlist(self, p):
        if hasattr(p, "exprlist"):
            return [p.expression, ] + p.exprlist
        elif hasattr(p, "expression"):
            return [p.expression, ]
        else:
            return []

    @ _('NAME ASSIGN expression')
    def statement(self, p):
        return Assigment(p.NAME, p.expression)

    @ _('type COLON NAME ASSIGN const')
    def statement(self, p):
        return Assigment(p.NAME, p.const, p.type)

    @ _('type COLON NAME ASSIGN expression')
    def statement(self, p):
        return Assigment(p.NAME, p.expression, p.type)

    @ _('U8', 'U16', 'U32', 'U64', 'S8', 'S16', 'S32', 'S64')
    def type(self, p):
        return Type(p[0])

    @ _('HEX', 'FLOAT', 'INTEGER', 'STRING', 'BOOLEAN')
    def const(self, p):
        return p[0]

    def error(self, p):
        raise SyntaxError(
            f"Syntax error at token {p.type} on line {p.lineno}, index {p.index} and value {p.value}")
