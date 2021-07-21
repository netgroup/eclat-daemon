"""Parser module

parse(eclat_script) -> Program

Program.exec() -> {
    programs: [LIST OF NAMES], 
    chains: {chain_name: c_code},
    loader: {name: ‘xdd’, ‘configuration: {...}’}
}


:raises Exception: [description]
:return: [description]
:rtype: [type]
"""

from rply import ParserGenerator
from parser.ast import *


def getEnvironment():
    class Environment(object):
        def __init__(self):
            self.variables = {}
    return Environment()


def getParser(syntax_tokens):
    package_name = "package_name"  # TBD
    pg = ParserGenerator(syntax_tokens,
                         precedence=[
                             ('left', [':']),
                             ('left', ['=']),
                             ('left', ['[', ']', ',']),
                             ('left', ['IF', 'ELSE', 'END',
                              'NEWLINE', 'WHILE', ]),
                             ('left', ['AND', 'OR', ]),
                             ('left', ['NOT', ]),
                             ('left', ['==', '!=', '>=', '>', '<', '<=', ]),
                             ('left', ['PIPE', ]),
                             ('left', ['^', ]),
                             ('left', ['&', ]),
                             ('left', ['>>', '<<', ]),
                             ('left', ['PLUS', 'MINUS', ]),
                             ('left', ['MUL', 'DIV', ]),
                         ])

    #################################################
    #                   PROGRAM                     #
    #################################################
    @pg.production("main : program")
    def main_program(p):
        return p[0]

    @pg.production('program : statement_full')
    def program_statement(p):
        return Program(p[0], package_name)

    @pg.production('program : statement_full program')
    def program_statement_program(p):
        if type(p[1]) is Program:
            program = p[1]
        else:
            program = Program(p[1], package_name)
        program.add_statement(p[0])
        return p[1]

    #################################################
    #                     BLOCK                     #
    #################################################
    @pg.production('block : INDENT blocks DEDENT')
    def block_expr(p):
        return p[1]

    @pg.production('blocks : statement_full')
    def blocks_expr(p):
        return Block(p[0])

    @pg.production('blocks : statement_full blocks')
    def blocks_expr_block(p):
        if type(p[1]) is Block:
            b = p[1]
        else:
            b = Block(p[1])
        b.add_statement(p[0])
        return b

    @pg.production('statement_full : statement NEWLINE')
    @pg.production('statement_full : statement $end')
    @pg.production('statement_full : statement')
    def statement_full(p):
        return p[0]

    @pg.production('statement : expression')
    def statement_expr(p):
        return p[0]

    #################################################
    #                    IMPORT                     #
    #################################################

    @pg.production('statement : FROM module_path IMPORT module_list')
    def statement_import_from(p):
        module_path = ".".join(p[1].get_statements())
        return FromImport(module_path, Array(p[3]))

    @pg.production('statement : IMPORT module_list')
    def statement_import(p):
        return Import(Array(p[1]))

    @pg.production('module_list : module_path')
    def import_from_module(p):
        module_path = ".".join(p[0].get_statements())
        return InnerArray([module_path])

    @pg.production('module_list : module_path , module_list')
    def import_from_module_list(p):
        module_path = ".".join(p[0].get_statements())
        p[2].push(module_path)
        return p[2]

    @pg.production('module_path : IDENTIFIER')
    def module_path(p):
        return InnerArray([p[0].getstr()])

    @pg.production('module_path : IDENTIFIER . module_path')
    def module_path(p):
        p[2].push(p[0].getstr())
        return p[2]

    #################################################
    #            VARIABLE DECLARATION               #
    #################################################

    @pg.production('statement : IDENTIFIER : type = expression')
    def statement_declaration_expression(p):
        return VariableDeclaration(Variable(p[0].getstr()), p[2].getstr(), p[4])

    @pg.production('statement : IDENTIFIER : type')
    def statement_declaration(p):
        return VariableDeclaration(Variable(p[0].getstr()), p[2].getstr())

    @pg.production('type : U8')
    @pg.production('type : U16')
    @pg.production('type : U32')
    @pg.production('type : U64')
    @pg.production('type : S8')
    @pg.production('type : S16')
    @pg.production('type : S32')
    @pg.production('type : S64')
    def statement_type(p):
        return p[0]

    #################################################
    #                 ASSIGNMENT                    #
    #################################################

    @pg.production('statement : IDENTIFIER = expression')
    def statement_assignment(p):
        return Assignment(p[1], Variable(p[0].getstr()), p[2])

    #################################################
    #            FUNCTION DECLARATION               #
    #################################################

    @pg.production('statement : DEF IDENTIFIER ( arglist ) : NEWLINE block ')
    def statement_func(p):
        return FunctionDeclaration(p[1].getstr(), Array(p[3]), p[7])

    @pg.production('arglist : IDENTIFIER')
    def arglist_single(p):
        return InnerArray([p[0]])

    @pg.production('arglist : IDENTIFIER , arglist')
    def arglist(p):
        p[2].push(p[0].getstr())
        return p[2]

    @pg.production('arglist : IDENTIFIER : type')
    def arglist_single(p):
        return InnerArray([p[2].getstr() + " " + p[0].getstr()])

    @pg.production('arglist : IDENTIFIER : type  , arglist')
    def arglist(p):
        p[4].push(p[2].getstr() + " " + p[0].getstr())
        return p[4]

    @pg.production('statement : DEF IDENTIFIER ( ) : NEWLINE block ')
    def statement_func_noargs(p):
        return FunctionDeclaration(p[1].getstr(), Null(), p[6])

    #################################################
    #                      IF                       #
    #################################################

    @pg.production('expression : IF expression : NEWLINE block elif_stmt')
    @pg.production('expression : IF expression : NEWLINE block else_stmt')
    @pg.production('expression : IF expression : NEWLINE block')
    def expression_if_else(p):
        if len(p) == 6:
            return If(condition=p[1], body=p[4], else_body=p[5])
        else:
            return If(condition=p[1], body=p[4])

    @pg.production('expression : IF expression : statement NEWLINE elif_stmt')
    @pg.production('expression : IF expression : statement NEWLINE else_stmt')
    @pg.production('expression : IF expression : statement_full')
    def expression_if_else_single_line(p):
        if len(p) == 6:
            return If(condition=p[1], body=p[3], else_body=p[5])
        else:
            return If(condition=p[1], body=p[3])

    #################################################
    #                    ELIF                       #
    #################################################
    @pg.production('elif_stmt : ELIF expression : NEWLINE block elif_stmt')
    @pg.production('elif_stmt : ELIF expression : NEWLINE block else_stmt')
    @pg.production('elif_stmt : ELIF expression : NEWLINE block')
    def elif_stmt(p):
        if len(p) == 6:
            return Elif(condition=p[1], body=p[4], else_body=p[5])
        else:
            return Elif(condition=p[1], body=p[4])

    @pg.production('elif_stmt : ELIF expression : statement NEWLINE elif_stmt')
    @pg.production('elif_stmt : ELIF expression : statement NEWLINE else_stmt')
    @pg.production('elif_stmt : ELIF expression : statement_full')
    def elif_stmt_single_line(p):
        if len(p) == 6:
            return Elif(condition=p[1], body=p[3], else_body=p[5])
        else:
            return Elif(condition=p[1], body=p[3])

    #################################################
    #                    ELSE                       #
    #################################################
    @pg.production('else_stmt : ELSE : statement_full')
    @pg.production('else_stmt : ELSE : NEWLINE block')
    def else_stmt(p):
        if len(p) == 3:
            return Else(else_body=p[2])
        else:
            return Else(else_body=p[3])

    #################################################
    #                    WHILE                      #
    #################################################

    @pg.production('expression : WHILE expression : NEWLINE block ')
    def expression_while(p):
        return While(condition=p[1], body=p[4])

    #################################################
    #                     FOR                       #
    #################################################
    # @pg.production('expression : FOR star_targets IN star_expressions : NEWLINE block ')
    # def expression_for(p):
    #     return For(star_targets=p[1], star_expressions=p[3], body=p[6])

    #################################################
    #                    RETURN                     #
    #################################################

    @pg.production('expression : RETURN')
    def statement_call_args(p):
        return Return(Null())

    @pg.production('expression : RETURN expression')
    def statement_call_args(p):
        return Return(p[1])

    @pg.production('expression : const')
    def expression_const(p):
        return p[0]

    #################################################
    #                     FLOAT                     #
    #################################################
    @pg.production('const : FLOAT')
    def expression_float(p):
        return Float(float(p[0].getstr()))

    #################################################
    #                    BOOLEAN                    #
    #################################################
    @pg.production('const : BOOLEAN')
    def expression_boolean(p):
        return Boolean(True if p[0].getstr() == 'true' else False)

    #################################################
    #                   INTEGER                     #
    #################################################
    @pg.production('const : INTEGER')
    def expression_integer(p):
        return Integer(int(p[0].getstr()), 10)

    @pg.production('const : HEX')
    def expression_integer(p):
        return Integer(int(p[0].getstr(), 16), 16)

    #################################################
    #                    STRING                     #
    #################################################
    @pg.production('const : STRING')
    def expression_string(p):
        return String(p[0].getstr().strip('"\''))

    #################################################
    #                  VARIABLE                     #
    #################################################
    @pg.production('expression : IDENTIFIER')
    def expression_call_noargs(p):
        return Variable(p[0].getstr())

    #################################################
    #                    CALL                       #
    #################################################
    # FIX DA FARE: CHIAMATA A CASCATA DEI METODI    #
    # per ora ce ne sono solo 2.                    #
    # Cioè (IDENTIFIER . IDENTIFIER)                #

    @pg.production('expression : IDENTIFIER ( )')
    def expression_call_noargs(p):
        return Call(p[0].getstr(), InnerArray())

    @pg.production('expression : IDENTIFIER . IDENTIFIER ( )')
    def expression_call_fun_noargs(p):
        return Call(p[0].getstr() + p[1].getstr() + p[2].getstr(), InnerArray())

    @pg.production('expression : IDENTIFIER ( expressionlist )')
    def expression_call_args(p):
        return Call(p[0].getstr(), p[2])

    @pg.production('expression : IDENTIFIER . IDENTIFIER ( expressionlist )')
    def expression_call_fun_noargs(p):
        return Call(p[0].getstr() + p[1].getstr() + p[2].getstr(), p[4])

    # @pg.production('expression : [ expression ]')
    # def expression_array_single(p):
    #     return Array(InnerArray([p[1]]))

    # @pg.production('expression : [ expressionlist ]')
    # def expression_array(p):
    #     return Array(p[1])

    #################################################
    #                 EXPRESSION                    #
    #################################################

    @pg.production('expression : ( expression )')
    def expression_parens(p):
        # in this case we need parens only for precedence
        # so we just need to return the inner expression
        return Expression(p[1])

    #################################################
    #                     NOT                       #
    #################################################
    @pg.production('expression : NOT expression ')
    def expression_not(p):
        return Not(p[1])

    #################################################
    #               BIT-WISE NOT                    #
    #################################################
    @pg.production('expression : ~ expression ')
    def expression_bitwise_not(p):
        return BitWise_Not(p[1])

    #################################################
    #               BINARY OPERATION                #
    #################################################

    @pg.production('expression : expression PLUS expression')  # +
    @pg.production('expression : expression MINUS expression')  # -
    @pg.production('expression : expression MUL expression')   # *
    @pg.production('expression : expression DIV expression')   # /
    @pg.production('expression : expression != expression')
    @pg.production('expression : expression == expression')
    @pg.production('expression : expression >= expression')
    @pg.production('expression : expression <= expression')
    @pg.production('expression : expression > expression')
    @pg.production('expression : expression < expression')
    @pg.production('expression : expression AND expression')
    @pg.production('expression : expression OR expression')
    # BITWISE OPERATION
    @pg.production('expression : expression & expression')     # AND
    @pg.production('expression : expression PIPE expression')  # OR
    @pg.production('expression : expression ^ expression')     # XOR
    @pg.production('expression : expression >> expression')    # SHIFT LEFT
    @pg.production('expression : expression << expression')    # SHIFT RIGHT
    def expression_binop(p):
        return BinaryOperation(operator=p[1].getstr(), left=p[0], right=p[2])

    @pg.production('expressionlist : expression')
    @pg.production('expressionlist : expression ,')
    def expressionlist_single(p):
        return InnerArray([p[0]])

    @pg.production('expressionlist : expression , expressionlist')
    def arglist(p):
        p[2].push(p[0])
        return p[2]

    # Error
    @pg.error
    def error_handle(token):
        raise Exception("Incorrect syntax, " + str(token) + " not recognized.")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pg.build()
