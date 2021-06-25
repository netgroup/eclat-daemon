import unittest
from engine import EclatEngine


class TestParser(unittest.TestCase):
    def test_parser_run_success(self):
        #import engine
        ee = EclatEngine()
        scriptfile = "test/test_eclat_code/test_2.eclat"
        with open(scriptfile, 'r') as f:
            script = f.read()
        ret = ee.run(script)
        self.assertEqual(ret, True)
