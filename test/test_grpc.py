import unittest


class TestGRPCRun(unittest.TestCase):
    def test_eclat_run_success(self):
        # TODO - old test script needs to be updated
        import eclat
        resp = eclat.run("test/eclat_scripts/ddos.eclat", "test")
        self.assertEqual(resp.status, "OK")
