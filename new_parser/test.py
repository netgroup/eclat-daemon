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
                #output += '\n'
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
            output += DEDENT + '\n'
        # print(output)
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
        NUMBER,  # Python decimals
        # STRING,  # single quoted strings only; syntax of raw strings
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
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ignore_comment = r'[ ]*\043[^\n]*'

    @_(r'0x[0-9a-fA-F]+', r'\d+')
    def NUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        else:
            t.value = int(t.value)
        return t

    # Line number tracking
    # @_(r'\n\s+')
    # def ignore_newline(self, t):
    #    self.lineno += t.value.count('\n')

    @_(r'\n')
    def NEWLINE(self, t):
        self.lineno += 1
        #t.value = 'NEWLINE'
        return t

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class EclatParser(Parser):
    tokens = EclatLexer.tokens

    precedence = (
    )

    def __init__(self):
        self.names = {}
        self.imports = []
        self.chains = {}

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
        pass

    @_('INDENT statements DEDENT')
    def block(self, p):
        pass

    @_('statement statements', 'statement')
    def statements(self, p):
        pass

    @_('PASS NEWLINE')
    def statement(self, p):
        pass

    @_('', 'NAME')
    def arglist(self, p):
        pass

    @_('FROM NAME IMPORT module_list')
    def import_stmt(self, p):
        # print(p)
        pass

    @_('NAME COMMA module_list',
       'NAME')
    def module_list(self, p):
        self.imports.append(p.NAME)
        return p


if __name__ == '__main__':
    lexer = EclatLexer()
    parser = EclatParser()
    prog = \
        """
# test
from gino import mario
from pablo import andrea, stefano
from kilo import etto , grammo

from package1 import p1

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
