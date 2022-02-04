#!/bin/bash

# Everything that is private to the bash process that will be launch
# mount the bpf filesystem.
# Note: childs of the launching (parent) bash can access this instance
# of the bpf filesystem. If you need to get access to the bpf filesystem
# (where maps are available), you need to use nsenter with -m and -t
# that points to the pid of the parent process (launching bash).

mount -t bpf bpf /sys/fs/bpf/             
mount -t tracefs nodev /sys/kernel/tracing

mkdir -p /sys/fs/bpf/{progs,maps}
# NOT an HIKe eBPF Program
mkdir -p /sys/fs/bpf/{progs/rawpass,}
bpftool prog loadall testbed/raw_pass.o /sys/fs/bpf/progs/rawpass type xdp
# Attach the (pinned) raw_pass program to netdev enp6s0f1 on the
# XDP hook.
bpftool net attach xdpdrv 				\
	pinned /sys/fs/bpf/progs/rawpass/xdp_pass	\
			dev enp6s0f1
