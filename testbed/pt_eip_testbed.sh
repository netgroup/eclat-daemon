#!/bin/bash

# this script needs to be executed from the eclat-daemon folder
# by calling:
# components/eip/testbed/pt_eip_testbed.sh
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

ECLAT_SCRIPT=components/eip/eclat_scripts/eip_pt.eclat

R1_COMMAND="tcpreplay -i i12 components/eip/pcaps/eip_cpt.pcap"
R1_EXEC=NO
MAIN_COMMAND="components/eip/scripts/enter-namespace-eip-pt-maps.sh"
MAIN_EXEC=NO
R4_COMMAND="tcpdump -ni i43 -w develop/trace-eip.pcap"
R4_EXEC=NO

source testbed/4r_common_testbed.sh
