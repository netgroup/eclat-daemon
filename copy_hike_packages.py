import json
import settings
import os
import shutil

PNAME_DEFAULT='hike_default'
DEFAULT_FILELIST=[
                'l2_redirect.bpf.c',
                'hike_drop.bpf.c',
                'hike_pass.bpf.c',
                'ip6_hset_srcdst.bpf.c',
                'lse.bpf.c',
                'monitor.bpf.c',
                'ip6_hset.h',
                '',
                '',
                ]

PNAME_METER='meter'
METER_FILELIST=[
                'ip6_dst_meter.bpf.c',
                'ip6_dst_tbmon.bpf.c',
                'ip6_sd_meter.bpf.c',
                'ip6_sd_tbmon.bpf.c',
                'ip6_alt_mark.bpf.c',
                'ip6_alt_mark.h',
                'tb_defs.h',
                '',
                '',
                ]

PNAME_SAMPLER='sampler'
SAMPLER_FILELIST=[
                'ip6_sd_dec2zero.bpf.c',      
                'tb_defs.h',
]

PNAME_ALTMARK='alt_mark'
ALTMARK_FILELIST=[
                'ip6_alt_mark.bpf.c',
                'ip6_alt_mark.h',                   
]

PNAME_INFO='info'
INFO_FILELIST=[
                'show_pkt_info.bpf.c',
                'tb_defs.h',
]


PNAME_MISC='misc'
MISC_FILELIST=[
                'udp_port.bpf.c',
]


class Copy_hike_packages:

    def packages_definitions(self):
        self.packages = []
        
        self.packages.append( {
            'package_name' : PNAME_DEFAULT,
            'package_files' : [
                {'source_folder' : self.hike_source_path, 
                'file_list' : DEFAULT_FILELIST
                }
            ]
        } )

        # self.packages.append( {
        #     'package_name' : PNAME_METER,
        #     'package_files' : [
        #         {'source_folder' : self.hike_contrib_source_path, 
        #         'file_list' : METER_FILELIST
        #         }
        #     ]
        # } )

        # self.packages.append( {
        #     'package_name' : PNAME_SAMPLER,
        #     'package_files' : [
        #         {'source_folder' : self.hike_contrib_source_path, 
        #         'file_list' : SAMPLER_FILELIST
        #         }
        #     ]
        # } )

        # self.packages.append( {
        #     'package_name' : PNAME_ALTMARK,
        #     'package_files' : [
        #         {'source_folder' : self.hike_contrib_source_path, 
        #         'file_list' : ALTMARK_FILELIST
        #         }
        #     ]
        # } )        

        # self.packages.append( {
        #     'package_name' : PNAME_INFO,
        #     'package_files' : [
        #         {'source_folder' : self.hike_contrib_source_path, 
        #         'file_list' : INFO_FILELIST
        #         }
        #     ]
        # } )

        # self.packages.append( {
        #     'package_name' : PNAME_MISC,
        #     'package_files' : [
        #         {'source_folder' : self.hike_contrib_source_path, 
        #         'file_list' : MISC_FILELIST
        #         }
        #     ]
        # } )

    def __init__(self):

        ###
        self.build_loaders_path = f"{settings.BUILD_LOADERS_DIR}/"
        self.build_programs_path = f"{settings.BUILD_PROGRAMS_DIR}/"
        self.build_chains_path = f"{settings.BUILD_CHAINS_DIR}/"

        self.hike_source_path = f"{settings.HIKE_SOURCE_PATH}/"
        self.hike_contrib_source_path = f"{settings.HIKE_CONTRIB_SOURCE_PATH}/"

        self.hike_programs_path = f"{settings.PROGRAMS_DIR}/"

        self.packages_definitions()

    def copy_packages(self):

        if not os.path.exists(self.hike_programs_path):
            print ("Path not found:",self.hike_programs_path)
            raise (IOError)
        for package in self.packages:
            pkg_path =f"{self.hike_programs_path}{package['package_name']}" 
            print (pkg_path)
            if not os.path.exists(pkg_path):
                os.makedirs(pkg_path)
            for pfiles in package['package_files']:
                for myfile in pfiles['file_list']:
                    if myfile != '' :
                        print (f"{pfiles['source_folder']}{myfile}")
                        shutil.copy2(f"{pfiles['source_folder']}{myfile}", pkg_path)

if __name__ == "__main__":

    c = Copy_hike_packages()
    c.copy_packages()

    #print (c.packages)


