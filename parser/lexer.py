from .eclat_ast import *
from sly import Lexer
import re


class IndentedLexer(Lexer):
    tokens = {}

    def preprocess(self, text):
        """
        Preprocess the file to:
        - convert tab in spaces
        - insert _INDENT and _DEDENT markers to ease the parsing phase
        - put _END at the end of the text
        """
        # convert tab in spaces
        text = text.replace('\t', '    ')
        # remove comments
        text = re.sub(re.compile("#.*?\n"), "", text)
        lines = text.split('\n')
        # put INDENT and DEDENT
        INDENT = "_INDENT"
        DEDENT = "_DEDENT"
        END = '_END'
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
        # output += ' ' + END
        print(output)
        return output

    def tokenize(self, text):
        return super().tokenize(self.preprocess(text))


class EclatLexer(IndentedLexer):
    tokens = {
        DEF,
        ELIF,
        IF,
        ELSE,
        WHILE,
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
        NEQ,
        LTE,
        GTE,
        LT,
        GT,
        ASSIGN,
        PLUS,
        MINUS,
        MULT,
        DIV,
        RETURN,
        NEWLINE,
        COMMA,
        INDENT,
        DEDENT,

        END
    }
    ignore = ' \t'

    # Tokens
    DEF = r'def'
    ELIF = r'elif'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
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
    NEQ = r'!='
    LTE = r'<='
    GTE = r'>='
    LT = r'<'
    GT = r'>'
    ASSIGN = r'='
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

    END = r'_END'
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
