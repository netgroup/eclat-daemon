import unittest
from parser.parser import EclatParser
from parser.lexer import EclatLexer


class TestParser(unittest.TestCase):
    def test_import(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
# test
from programs.package1 import program1
from programs.package2 import program1, program2, program3
from programs.package3 import program1 , program2

def chain1():

    
    pass

def chain2():
    pass
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print(parser.imports)
        self.assertEqual(parser.imports['programs']['package1'], ['program1'])
        self.assertEqual(sorted(parser.imports['programs']['package2']), sorted([
            'program3', 'program2', 'program1']))
        self.assertEqual(sorted(parser.imports['programs']['package3']), sorted(
            ['program2', 'program1']))
        # print(parser.chains)
        # print(p)

    def test_function_call(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """from programs.hike import drop

def mychain0():
    u8 : b = 9
    drop(b)
    drop(0.1)
    drop(1,2,3, b)
    b = drop()
    u16: x = drop()
    pass
    if x:
        return 1
    return 1
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
        self.assertEqual(
            parser.chains['mychain1'].arguments[0].type.type, 'u8')
        self.assertEqual(
            parser.chains['mychain1'].arguments[0].name, 'pippo')
        self.assertEqual(
            parser.chains['mychain1'].arguments[1].type.type, 'u16')
        self.assertEqual(
            parser.chains['mychain1'].arguments[1].name, 'pluto')

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
    p = 2 != 2
    p = 2 % 2
    p = (1+1) == 2
    p = 2 and 2
    p = 2 or 2
    p = not 2
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_bitwise(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
def mychain():
    #types
    s8 : p = 12
    s16 : p = 12
    s32 : p = 12
    s64 : p = 12
    u8 : p = 12
    u16 : p = 12
    u32 : p = 12
    u64 : p = 12
    # unary operations
    p = -p
    p = ~p
    # bitwise 
    p = p & p
    p = p | p
    p = p ^ p
    # bit shifting
    p = p << 3
    p = p >> 4
    p = p >> w
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        chain_code = p['chains']['mychain'].to_c('test_package')
        self.assertIn('p = -p', chain_code)
        self.assertIn('p = ~p', chain_code)
        self.assertIn('p = p & p', chain_code)
        self.assertIn('p = p | p', chain_code)
        self.assertIn('p = p ^ p', chain_code)
        self.assertIn('p = p << 3', chain_code)
        self.assertIn('p = p >> 4', chain_code)

    def test_if(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
def mychainIF():
    a = 2 + 2
    if p == 3:
        pass
        b = 2
    elif p == 2:
        pass
        c = 4 * 3
    a = 3 + 2

    if p == 3:
        pass
    a = 5 + 2
    if p == 2:
        pass
    else:
        p = 1

# if indent this comment -> error
    pass
    if p == 2:
        pass
        pass
    elif p == 2:
        pass
        pass
    elif p == 9:
        pass
        pass
    else:
        pass
        pass
# nested if
    if p == 2:
        pass
        if p == 4:
            pass
    if p == 20:
        pass
"""
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_while(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
def mychain_while():
    while 5 == 5:
        pass
"""
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_indentation(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
#putting comments with random indentation should not affect the code
    #ddd  
def mychain_indent():
    while 5 == 5:
        pass


    while 1 == 1:
        if (1 == 2):
            pass
                #daaaaa
        #ddd
          #ddd
#ddd
    #xxx
    """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)

    def test_globals(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
u8 : a = 1
def mychain_globals():
    while a == 5:
        pass
    """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        parser.parse(tokens)
        print(parser.globals)

    def test_objects(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet
def mychain():
    Packet.readU16(12)
    pass
    """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        parser.parse(tokens)
        print(parser.globals)

    def test_code1(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet
from programs.net import drop, allow
from programs.test import funzione1, fun_funzion1

def mychain0():
    eth_type = Packet.readU16(12)
    if eth_type == 0x86dd:
        ttl = Packet.readU8(21)
        if ttl == 64:
            Packet.writeU8(17,21) 
            funzione1(pippo)
            fun_funzion1(par1, pippo)
        
    
    if eth_type == 0x800 :
        drop(eth_type)
        pass
        return
        

    allow(eth_type)
    return
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print("p=", p)
        print(parser.globals)

    def test_arglist(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet
def mychain0(u8 : a, u8 : b):
    pass
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print("p=", p)
        print(parser.globals)

    def test_loader(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet, Loader
from programs.net import drop, allow
from programs.test import funzione1, fun_funzion1
from loaders.pippo import ipv6_classifier

ipv6_classifier.attach('enp6s0f0', 'xdp')

def mychain0():
    eth_type = Packet.readU16(12)
    if eth_type == 0x86dd :
        ttl = Packet.readU8(21)
        if ttl == 64:
            Packet.writeU8(17,21) 
            funzione1(pippo)
            fun_funzion1(par1, pippo)
        
    
    if eth_type == 0x800 :
        drop(eth_type)
        pass
        return
        

    allow(eth_type)
    return
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print("p=", p)
        print(parser.globals)

    def test_map_config(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet, Loader
from programs.net import drop, allow
from programs.test import funzione1, fun_funzion1
from loaders.pippo import ipv6_classifier

ipv6_classifier.attach('enp6s0f0', 'xdp')

ipv6_simple_classifier[ipv6_simple_classifier_map1] = { (0): (MYCHAIN) }
ipv6_simple_classifier[ipv6_simple_classifier_map2] = { (0): (MYCHAIN), (1,2,3): (MYCHAIN2) }

ipv6_simple_classifier[ipv6_simple_classifier_map3] = {
    (192,168,1,1): (mychain2), 
    (192,168,1,2): (mychain10)
}
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print("p=", p)
        print(parser.globals)
        self.assertIn({'program_name': 'ipv6_simple_classifier',
                      'map_name': 'ipv6_simple_classifier_map1', 'data': {('0',): ['MYCHAIN']}}, parser.maps)
        self.assertIn({'program_name': 'ipv6_simple_classifier',
                      'map_name': 'ipv6_simple_classifier_map3', 'data': {('192', '168', '1', '1'): ['mychain2'], ('192', '168', '1', '2'): ['mychain10']}}, parser.maps)

    def test_constant(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet, Loader
from programs.net import drop, allow
from programs.test import funzione1, fun_funzion1
from loaders.pippo import ipv6_classifier

ipv6_classifier.attach('enp6s0f0', 'xdp')


def mychain0():
    CONST1 = 10;CONST2 = 0x800;CONST4=1
    
    NONConst3 = 10
    eth_type = Packet.readU16(12)
    if eth_type == 0x86dd :
        ttl = Packet.readU8(21)
        if ttl == 64:
            Packet.writeU8(17,21) 
            funzione1(pippo)
            fun_funzion1(par1, pippo)
        
    
    if eth_type == CONST2 :
        drop(CONST1)
        pass
        return
        

    allow(eth_type)
    return
        """
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        p = parser.parse(tokens)
        print("p=", p)
        print(p['chains']['mychain0'].to_c("mypackage"))
        print(parser.globals)
        print("parsed constants")
