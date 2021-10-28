import unittest
from controller import EclatController


class TestController(unittest.TestCase):
    def test_controller1(self):
        controller = EclatController()
        script = """
from programs.hike import Packet
from loaders.pippo import ipv6_classifier

ipv6_classifier.attach('enp6s0f0', 'xdp')
#ipv6_classifier[mapname] = {'key': value}
        """
        print(script)
        controller.load_configuration(script)
