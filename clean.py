import json
import settings
import os

class Clean:

    def __init__(self):

        ###
        self.build_loaders_path = f"{settings.BUILD_LOADERS_DIR}/"
        self.build_programs_path = f"{settings.BUILD_PROGRAMS_DIR}/"
        self.build_chains_path = f"{settings.BUILD_CHAINS_DIR}/"


    def clean(self):
        if os.path.exists(self.build_loaders_path):
            print(self.build_loaders_path)
            os.system(f"cd {self.build_loaders_path} && ls -la && rm -rf *")
        if os.path.exists(self.build_programs_path):
            print(self.build_programs_path)
            os.system(f"cd {self.build_programs_path} && ls -la && rm -rf *")
        if os.path.exists(self.build_chains_path):
            print(self.build_chains_path)
            os.system(f"cd {self.build_chains_path} && ls -la && rm -rf *")

if __name__ == "__main__":

    c = Clean()
    c.clean()


