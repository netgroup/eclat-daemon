#! /bin/bash

cd /opt/eclat-daemon
mkdir -p /sys/fs/bpf/{progs/rawpass,}
make -f hike/external/Makefile prog HIKE_DIR=hike/src HIKE_CFLAGS='-D__HIKE_CFLAGS_EXTMAKE' SRC_DIR=hike/src/ PROG=raw_pass.bpf.c BUILD=hike/src/.output
bpftool prog loadall testbed/raw_pass.o /sys/fs/bpf/progs/rawpass type xdp
bpftool net attach xdpdrv pinned /sys/fs/bpf/progs/rawpass/xdp_pass dev enp6s0f1

