import unittest
from controller import EclatController
from chainloader import ChainLoader
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
