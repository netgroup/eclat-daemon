#!/bin/bash

# this script needs to be executed from the eclat-daemon folder
# by calling:
# testbed/basic_testbed.sh
# This script executes a HIKe program that can extract some information
# from the packet and display it in a log. For example, it can display
# transport ports for UDP or TCP packets.
#                                               To be Natted in the host
#                                                         | Host 192.168.77.1
#                                                         |
#                                                     HOSTBRIDGE
#                                                         | Host 192.168.77.2
#                                                         |
#                     +------------------+      +------------------+
#                     |        TG        |      |       SUT        |
#                     |                  |      |                  |
#                     |         enp6s0f0 +------+ enp6s0f0 <--- HIKe VM XDP loader
#                     |                  |      |                  |
#                     |                  |      |                  |
#                     |         enp6s0f1 +------+ enp6s0f1         |
#                     |                  |      |         + cl0  <-|- towards the collector
#                     +------------------+      +---------|--------+
#                                                         |
#                                               +---------|------+
#                                               |         + veth0|
#                                               |                |
#                                               |    COLLECTOR   |
#                                               +----------------+

ECLAT_SCRIPT=test/eclat_scripts/basic_example.eclat

DEBUG_COMMAND="scripts/enter-namespace-debug-no-vm.sh"
DEBUG_EXEC=YES

MAPS_COMMAND="scripts/enter-namespace-watchmap.sh"
MAPS_EXEC=YES

CLT_COMMAND="tcpdump -i veth0"
CLT_EXEC=YES

TG1_COMMAND="tcpreplay -i enp6s0f0 hike/testbed/pkts/pkt_ipv6_udp.pcap"
TG1_EXEC=NO

TG2_COMMAND="ping -i 5 fc01::3"
TG2_EXEC=NO

source testbed/common_testbed.sh
