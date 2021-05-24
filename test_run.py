import unittest


class TestAddFishToAquarium(unittest.TestCase):
    def test_eclat_run_success(self):
        import eclat
        resp = eclat.run("testscript.eclat")
        self.assertEqual(resp.status, "OK")
