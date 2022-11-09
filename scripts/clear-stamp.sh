#!/bin/bash

cd /sys/fs/bpf/progs/
rm -rf *

cd /sys/fs/bpf/maps/
rm -rf *

cd /opt/eclat-daemon/components/
rm -rf stamp/build test/

cd /opt/eclat-daemon/hike_v3/src/.output/
rm -rf *

bpftool net detach xdp dev enp6s0f0
bpftool net detach xdp dev enp6s0f1

