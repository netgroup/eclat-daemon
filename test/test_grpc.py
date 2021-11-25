import unittest


class TestGRPCRun(unittest.TestCase):
    def test_eclat_run_success(self):
        import eclat
        resp = eclat.run("test/eclat_scripts/ddos.eclat", "test")
        self.assertEqual(resp.status, "OK")
