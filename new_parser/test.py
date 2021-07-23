from ast import *
#from new_parser.ast import Argument, Statement
from sly import Lexer, Parser
import re


class IndentedLexer(Lexer):
    tokens = {}

    def preprocess(self, text):
        """
        Preprocess the file to:
        - convert tab in spaces
        - insert _INDENT and _DEDENT markers to ease the parsing phase
        """
        # convert tab in spaces
        text = text.replace('\t', '    ')
        # remove comments
        text = re.sub(re.compile("#.*?\n"), "", text)
        lines = text.split('\n')
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
                # output += '\n'
                continue

            initial_spaces = len(line) - len(line.lstrip(' '))
            if initial_spaces > curr_indentation_level:
                indentations.append(initial_spaces)
                output += INDENT + line + '\n'
                print("indenting of {} space. Current indentation was {}".format(
                    initial_spaces, curr_indentation_level))
            elif initial_spaces < curr_indentation_level:
                indentations.pop()
                expected_spaces = indentations[-1]
                if expected_spaces != initial_spaces:
                    raise Exception("Syntax error on line {}: expected {} space for deindent ({} received)".format(
                        lineno, expected_spaces, initial_spaces))
                output += DEDENT + '\n' + line + '\n'
            else:
                output += line + '\n'
            curr_indentation_level = initial_spaces
        # fill the remaining intendation
        while (len(indentations) > 1):
            indentation = indentations.pop()
            output += DEDENT + '\n'
        print(output)
        return output

    def tokenize(self, text):
        return super().tokenize(self.preprocess(text))


class EclatLexer(IndentedLexer):
    tokens = {
        DEF,
        IF,
        FROM,
        IMPORT,
        PASS,
        NAME,
        # types
        U8,
        U16,
        U32,
        U64,
        S8,
        S16,
        S32,
        S64,
        # constants
        HEX,
        FLOAT,
        INTEGER,
        STRING,
        BOOLEAN,

        # NUMBER,  # Python decimals
        LPAR,
        RPAR,
        COLON,
        EQ,
        ASSIGN,
        LT,
        GT,
        PLUS,
        MINUS,
        MULT,
        DIV,
        RETURN,
        NEWLINE,
        COMMA,
        INDENT,
        DEDENT
    }
    ignore = ' \t'

    # Tokens
    DEF = r'def'
    IF = r'if'
    FROM = r'from'
    IMPORT = r'import'
    PASS = r'pass'
    LPAR = r'\('
    RPAR = r'\)'
    RETURN = r'return'
    INDENT = r'_INDENT'
    DEDENT = r'_DEDENT'
    COLON = r':'
    EQ = r'=='
    ASSIGN = r'='
    LT = r'<'
    GT = r'>'
    PLUS = r'\+'
    MINUS = r'-'
    MULT = r'\*'
    DIV = r'/'
    COMMA = r','

    U8 = r'u8'
    U16 = r'u16'
    U32 = r'u32'
    U64 = r'u64'
    S8 = r's8'
    S16 = r's16'
    S32 = r's32'
    S64 = r's64',
    HEX = r'0[xX][0-9a-fA-F]+(?!\w)'
    FLOAT = r'-?\d+\.\d+'
    INTEGER = r'-?\d+'
    STRING = r'(""".*?""")|(".*?")|(\'.*?\')'
    BOOLEAN = r'true(?!\w)|false(?!\w)'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ignore_comment = r'[ ]*\043[^\n]*'

    # @_(r'0x[0-9a-fA-F]+', r'\d+')
    # def NUMBER(self, t):
    #    if t.value.startswith('0x'):
    #        t.value = int(t.value[2:], 16)
    #    else:
    #        t.value = int(t.value)
    #    return t

    # Line number tracking
    # @_(r'\n\s+')
    # def ignore_newline(self, t):
    #    self.lineno += t.value.count('\n')

    @_(r'\n')
    def NEWLINE(self, t):
        self.lineno += 1
        # t.value = 'NEWLINE'
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class EclatParser(Parser):
    tokens = EclatLexer.tokens

    precedence = (
    )

    def __init__(self):
        self.imports = []
        self.chains = {}
        self.loaders = {}
        # stack for the parser
        self.statement_list = []
        self.argument_list = []

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
        # print(p)
        pass

    @_('NAME COMMA module_list',
        'NAME')
    def module_list(self, p):
        self.imports.append(p.NAME)
        return p

    ########### TODO #########
    # expression
    # statements: if, while, for, return

    # chiamare i moduli
    # modificare mappe (?)

    # const
    # variabili globali


if __name__ == '__main__':
    lexer = EclatLexer()
    parser = EclatParser()
    prog = """
# test
from gino import mario
from pablo import andrea, stefano
from kilo import etto , grammo

from package1 import p1

def chain1():
  a = 2
  pass

def chain2():
    u8 : b = 7

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
