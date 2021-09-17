import unittest
from controller import EclatController


class TestController(unittest.TestCase):
    def test_controller1(self):
        controller = EclatController()
        scriptfile = "test/test_eclat_code/test_1.eclat"
        with open(scriptfile, 'r') as f:
            script = f.read()
        print("Passing to the controller the following script:")
        script = """
from hike import drop

def mychain0():
    drop()
        """
        print(script)
        controller.load_configuration(script)
