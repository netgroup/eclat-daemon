#!/bin/bash

# this script needs to be executed from the eclat-daemon folder
# by calling:
# testbed/pt_eip_testbed.sh
#
# topology:
#
#      +------------------+      +------------------+      +------------------+      +------------------+
#      |        r1        |      |        r2        |      |        r3        |      |        r4        |
#      |                  |      |                  |      |                  |      |                  |
#      |              i12 +------+ i21          i23 +------+ i32          i34 +------+ i43              |
#      |                  |      |                  |      |                  |      |                  |
#      |                  |      |                  |      |                  |      |                  |
#      +------------------+      +------------------+      +------------------+      +------------------+
#

ECLAT_SCRIPT=test/eclat_scripts/eip_timestamps.eclat


source testbed/eip_common_testbed.sh
