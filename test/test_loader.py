import unittest
from controller import EclatController
from chainloader import ChainLoader
import settings


class TestLoader(unittest.TestCase):
    def test_loader(self):
        cl = ChainLoader(name="minimal_loader", package="basic")
        cl.clean()
        cl.compile()
        cl.load()
        cl.attach("ip6tnl0")
