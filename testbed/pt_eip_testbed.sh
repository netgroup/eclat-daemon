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

ECLAT_SCRIPT=test/eclat_scripts/eip_pt.eclat

R1_COMMAND="tcpreplay -i i12 hike_v3/testbed/pkts/eip_cpt.pcap"
R1_EXEC=NO
MAIN_COMMAND="scripts/enter-namespace-eip-pt-maps.sh"
MAIN_EXEC=NO
R4_COMMAND="tcpdump -ni i43 -w develop/trace-eip.pcap"
R4_EXEC=NO

source testbed/eip_common_testbed.sh
