#!/bin/bash

# this script needs to be executed from the eclat-daemon folder
# by calling:
# testbed/testbed.sh [script.eclat] [TG1_COMMAND] [TG2_COMMAND]
# [script.eclat] defaults to test/eclat_scripts/basic_example.eclat
# [TG1_COMMAND] defaults to "tcpreplay -i enp6s0f0 hike/testbed/pkts/pkt_ipv6_udp.pcap"
# [TG2_COMMAND] defaults to "ping -i 0.5 fc01::3"

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


if [[ $1 ]] ; then
	ECLAT_SCRIPT="$1"
else 
	ECLAT_SCRIPT=test/eclat_scripts/basic_example.eclat
fi

DEBUG_COMMAND="scripts/enter-namespace-debug-no-vm.sh"
DEBUG_EXEC=YES

MAPS_COMMAND="scripts/enter-namespace-watchmap.sh"
MAPS_EXEC=YES

CLT_COMMAND="tcpdump -i veth0"
CLT_EXEC=YES

if [[ $2 ]] ; then
	TG1_COMMAND="$2"
else 
	TG1_COMMAND="tcpreplay -i enp6s0f0 hike/testbed/pkts/pkt_ipv6_udp.pcap"
fi
TG1_EXEC=NO

if [[ $3 ]] ; then
	TG2_COMMAND="$3"
else
	TG2_COMMAND="ping -i 0.5 fc01::3"
fi

TG2_EXEC=NO

source testbed/common_testbed.sh
