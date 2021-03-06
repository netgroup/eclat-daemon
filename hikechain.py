import cal
import settings
import os


class HikeChain:
    """
    An HIKe Chain is a composition of programs.
    It runs in the HIKe VM.
    """

    def __init__(self, name, package, code="", globals=None):
        self.name = name
        self.package = package  # can be the (file) name of the script
        self.code = code
        self.globals = globals
        ###
        self.src_file_path = f"{settings.COMPONENTS_DIR}/{self.package}/{name}.hike.c"
        self.obj_file_path = f"{settings.COMPONENTS_DIR}/{self.package}/build/{name}.hike.o"
        self.is_compiled = self._is_compiled()
        self.is_linked = self._is_linked()

    def _is_compiled(self):
        return os.path.exists(self.obj_file_path)

    def _is_linked(self):
        return os.path.exists(self.src_file_path)

    def link(self, registered_ids):
        """
        Resolve symbols for program IDs.
        Write to a file.
        Programs maps is a tuple of (package, function, id)
        """
        print("Linking chain...")
        mapper_code = []
        # create the define list with the registered id
        for el in registered_ids:
            if el['type'] == 'program':
                placeholder = f"hike_ebpf_prog_{el['package']}_{el['name']}".upper(
                )
                mapper_code.append(f"#define {placeholder} {el['id']}")
            elif el['type'] == 'chain':
                placeholder = f"hike_chain_{el['package']}_{el['name']}".upper(
                )
                mapper_code.append(f"#define {placeholder} {el['id']}")
            else:
                raise Exception("Invalid mapping entry.")
        headers = """
#include <linux/errno.h>
#include "hike_vm.h"
#include "parse_helpers.h"

        """
        self.code = headers + "\n".join(mapper_code) + "\n" + self.code
        self.is_linked = True

        if not os.path.exists(os.path.dirname(self.src_file_path)):
            # create directory if not exists
            os.mkdir(os.path.dirname(self.src_file_path))

        with open(self.src_file_path, "w") as f:
            f.write(self.code)
        cal.format_c(self.src_file_path)
        print(f"Linked!\n{self.code}")

    def compile(self):
        if not os.path.exists(self.src_file_path):
            raise Exception(
                f"Compilation failed. File {self.src_file_path} does not exist.")
        if not self.is_linked:
            raise Exception(
                f"Compilation failed. Chain {self.name} must be linked before compilation.")
        # if not self.is_compiled:
        cal.make_hike_chain(self.src_file_path)
        self.is_compiled = True
        # else:
        #    print(f"Hike chain {self.name} is already compiled")

    def clean(self):
        if os.path.exists(self.obj_file_path):
            os.remove(self.obj_file_path)
        if os.path.exists(self.src_file_path):
            os.remove(self.src_file_path)
        self.is_compiled = False
        self.is_linked = False

    def load(self):
        if not self.is_compiled:
            raise Exception("Can not register a uncompiled chain")
        cal.hikecc(self.name, self.package)

    def unload(self):
        pass
