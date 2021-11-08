import unittest
from controller import EclatController
from chainloader import ChainLoader
from parser.parser import EclatParser
from parser.lexer import EclatLexer
import settings
import cal


class TestLoader(unittest.TestCase):
    def setUp(self):
        cal.ebpf_system_init()
        cal.hike_system_init()
        return super().setUp()

    def test_loader(self):
        cl = ChainLoader(name="minimal_loader", package="basic")
        cl.clean()
        cl.compile()
        cl.load()
        cl.attach("ip6tnl0")

    def test_parsing(self):
        lexer = EclatLexer()
        parser = EclatParser()
        prog = """
from programs.hike import Packet, Loader
from programs.net import drop, allow
from programs.test import funzione1, fun_funzion1
from loaders.basic import ip6_simple_classifier

ip6_simple_classifier.attach('enp6s0f0', 'xdp')

ip6_simple_classifier[ipv6_simple_classifier_map] = { (0): (86) }
#minimal_loader[ipv6_simple_classifier_map] = { (0): (MYCHAIN), (1,2,3): (MYCHAIN2) }

#minimal_loader[ipv6_simple_classifier_map3] = {
#    (192,168,1,1): (mychain2), 
#    (192,168,1,2): (mychain10)
#}
"""
        tokens = lexer.tokenize(prog)
        for tok in tokens:
            print(tok)
        tokens = lexer.tokenize(prog)
        parser.parse(tokens)
        print(parser.globals)

        loader = parser.loaders[0]
        # get the package
        print(loader)
        name, package, attach_type, dev = loader['name'], loader[
            'package'], loader['attach_type'], loader['dev']

        cl = ChainLoader(name, package)
        cl.clean()
        cl.compile()
        cl.load()
        # cl._get_maps()
        print(f"maps info: {cl.maps_info}")

        # cl.attach("enp6s0f0")
        print(f"parser maps: {parser.maps}")
        for map_configuration in filter(lambda x: x['program_name'] == name, parser.maps):
            for key, value in map_configuration['data'].items():
                print(
                    f"Writing map {map_configuration['map_name']} with {key}, {value}")
                cl.write_map(map_configuration['map_name'], key, value)
