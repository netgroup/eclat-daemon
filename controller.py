from cal import ebpf_system_init, hike_system_init
from hikeprogram import HikeProgram


class EclatController:
    hike_programs = {}

    def __init__(self):
        ebpf_system_init()
        hike_system_init()

    def load_hike_program(self):
        PROG_NAME = 'testprog'
        PROG_PKG = 'testpkg'
        if 'testprog' not in self.hike_programs.keys():
            self.hike_programs['test'] = HikeProgram(PROG_NAME, PROG_PKG)
        p = self.hike_programs['test']
        p.pull()
