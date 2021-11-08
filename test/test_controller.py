import unittest
from controller import EclatController
import cal


class TestController(unittest.TestCase):
    def setUp(self):
        cal.ebpf_system_init()
        cal.hike_system_init()
        return super().setUp()

    def test_scenario_ddos(self):
        cal.ebpf_system_init()
        cal.hike_system_init()
        controller = EclatController()
        package = "ddos_pkg"
        script = """
from programs.net import hike_drop, hike_pass, ip6_hset_srcdst, lse, monitor
from loaders.basic import ip6_sc

ip6_sc[ipv6_sc_map] = { (0): (6) }
ip6_sc.attach('enp6s0f0', 'xdp')

def ddos():
    u64 : rs = ip6_hset_srcdst(2)
    if not rs:
        monitor(1)
        hike_drop()
        return 0

    u64 : ts = lse()
    if ts < 500000000:
        ip6_hset_srcdst(1)
        hike_drop()
        return 0
    
    monitor(0)
    hike_pass()
        """
        print(script)
        controller.load_configuration(script, package)
