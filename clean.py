import json
import settings
import os

# Cleans up all the object files in the folders of the components

class Clean:

    def __init__(self):
        pass

    def clean(self):
        os.system(
            f'find {settings.COMPONENTS_DIR} -iname "*.o" -type f -exec rm -v {{}} \; 2>/dev/null')


if __name__ == "__main__":

    c = Clean()
    c.clean()
