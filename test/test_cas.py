import unittest
import cas
import settings
import os


class TestCas(unittest.TestCase):
    def test_make_hike_chain(self):
        hike_source_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime/output/eclat_output.hike.c")
        makefile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.EXTERNAL_MAKEFILE_PATH)
        hike_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.HIKE_SOURCE_PATH)
        ret = make_hike_chain(makefile, hike_source_file, hike_dir)
        self.assertEqual(ret, True)
    

    def test_make_ebpf_hike_program(self):
        hike_source_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime/output/minimal_xdp.bpf.c")
        makefile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.EXTERNAL_MAKEFILE_PATH)
        hike_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), settings.HIKE_SOURCE_PATH)
        ret = make_ebpf_hike_program(makefile, hike_source_file, hike_dir)
        self.assertEqual(ret, True)
    

    def test_hikecc_load(self):
        # assert: Esiste la mappa hike_chain_map
        path_eclat_output = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime/output/build/eclat_output.hike.o")
        map_name = "hike_chain_map"
        loader_file = cas.hikecc(path_eclat_output, map_name)
        ret = load_chain(loader_file)
        self.assertEqual(ret, True)
    
    def test_bpftool_prog_loadall(self):
        bpf_source_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime/output/build/minimal_xdp.bpf.o")
        ret = bpftool_prog_loadall(bpf_source_file, settings.BPF_FS_PROGS_PATH, type="xdp", pinmaps_map_dir=settings.BPF_FS_MAPS_PATH)
        self.assertEqual(ret, True)
    
    def test_bpftool_prog_load(self):
        bpf_source_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runtime/output/xdp_pass.o")
        ret = bpftool_prog_load(bpf_source_file, settings.BPF_FS_PROGS_PATH, type="xdp", pinmaps_map_dir=settings.BPF_FS_MAPS_PATH)
        self.assertEqual(ret, True)
    

    def test_bpftool_net_attach(self):
        ret = bpftool_net_attach("xdpdrv", "enp6s0f0", prog="pinned /sys/fs/bpf/progs/xdp_pass")
        self.assertEqual(ret, True)
    
    def test_bpftool_net_attach(self):
        map_name = settings.BPF_FS_MAPS_PATH + "/" + "map_1"
        ret = bpftool_net_attach("pinned " + map_name, key_data="key hex 0b 00 00 00", value="value	pinned /sys/fs/bpf/progs/net/hvxdp_allow_any")
        self.assertEqual(ret, True)
    



    
    