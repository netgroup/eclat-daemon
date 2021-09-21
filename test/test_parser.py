import unittest
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class TestParser(unittest.TestCase):
    def test_import(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
# test
from package1 import program1
from package2 import program1, program2, program3
from package3 import program1 , program2

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
        self.assertEqual(parser.imports['package1'], ['program1'])
        self.assertEqual(sorted(parser.imports['package2']), sorted([
            'program3', 'program2', 'program1']))
        self.assertEqual(sorted(parser.imports['package3']), sorted(
            ['program2', 'program1']))
        # print(parser.chains)
        # print(p)

    def test_function_call(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """from hike import drop

def mychain0():
    u8 : b = 9
    drop(b)
    drop(0.1)
    drop(1,2,3, b)
    b = drop()
    u16: x = drop()
    pass
        """
        #tokens = lexer.tokenize(prog)
        # for tok in tokens:
        #    print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_chain_parameters(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """def mychain1(u8 : pippo, u16: pluto):
    pass
    """
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_expression(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
def mychain():
    u8 : p = 1
    p = 3 + 2
    p = 0.1 - 5.4
    p = 2 / 2.0
    p = 4 * 2
    p = 2 > 2
    p = 2 < 2
    p = 2 >= 2
    p = 2 <= 2
    p = 2 == 2
        """

        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
