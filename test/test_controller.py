import unittest
from controller import EclatController


class TestController(unittest.TestCase):
    def test_scenario_ddos(self):
        controller = EclatController()
        script = """
from loaders.basic import ip6_simple_classifier
from programs.net import hike_drop, hike_pass, ip6_hset_srcdst, lse, monitor

ip6_simple_classifier[ipv6_simple_classifier_map] = { (0): (86) }
ip6_simple_classifier.attach('enp6s0f0', 'xdp')

def ddos():
    u64 : rs = ip6_hset_srcdst(2)
    if !rs:
        monitor(1)
        hike_drop()

    u64 : ts = lse()
    if ts < 500000000:
        ip6_hset_srcdst(1)
        hike_drop()
    
    monitor(0)
    hike_pass()
        """
        print(script)
        controller.load_configuration(script)
