import unittest


class TestGRPCRun(unittest.TestCase):
    def test_eclat_run_success(self):
        import eclat
        resp = eclat.run("testscript1.eclat")
        self.assertEqual(resp.status, "OK")
