import unittest
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class TestParser(unittest.TestCase):
    def test_parsing_import(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
# test
from gino import mario
from pablo import andrea, stefano, pino
from kilo import etto , grammo

from package1 import p1

def chain1():
a = 2
pass

def chain2():
    u8 : b = 7
        """
        prog = """
from hike import drop

def mychain0():
    drop()
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print(parser.imports)
        print(parser.chains)
        print(p)
        # todo ripulire
