from parser.json_parser import parse_info
import unittest
import settings
import os


class TestJSONParser(unittest.TestCase):
    def test_json_parser(self):
        INPUT_FILE = f'{settings.HIKE_SOURCE_PATH}/.output/ip6_simple_classifier.bpf.json'
        print(f"Loading {INPUT_FILE}")
        self.assertTrue(os.path.exists(INPUT_FILE))
        maps_info = []
        hike_program_info = {}
        (maps_info, hike_program_info) = parse_info(INPUT_FILE)

        print(maps_info)
        print(hike_program_info)


# INPUT_FILE='ip6_hset_srcdst.bpf.json'

# usage example
