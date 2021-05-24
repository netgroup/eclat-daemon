import unittest


class TestParser(unittest.TestCase):
    def test_parser_run_success(self):
        import engine
        ee = EclatEngine()
        scriptfile = "testscript1.eclat"
        with open(scriptfile, 'r') as f:
            script = f.read()

            self.assertEqual(ee.run(script), True)
