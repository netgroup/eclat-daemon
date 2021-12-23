#!/bin/bash

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

TMUX=ebpf
IPP=ip

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

# Clean up previous network namespaces
ip -all netns delete

ip netns add tg
ip netns add sut
ip netns add clt

ip -netns tg link add enp6s0f0 type veth peer name enp6s0f0 netns sut
ip -netns tg link add enp6s0f1 type veth peer name enp6s0f1 netns sut

ip -netns sut link add cl0 type veth peer name veth0 netns clt

###################
#### Node: TG #####
###################
echo -e "\nNode: TG"

ip -netns tg link set dev lo up

ip -netns tg link set dev enp6s0f0 address 00:00:00:00:01:00
ip -netns tg link set dev enp6s0f1 address 00:00:00:00:01:01

ip -netns tg link set dev enp6s0f0 up
ip -netns tg link set dev enp6s0f1 up

ip -netns tg addr add 12:1::1/64 dev enp6s0f0
ip -netns tg addr add fc01::1/64 dev enp6s0f0
ip -netns tg addr add fc02::1/64 dev enp6s0f0
ip -netns tg addr add 10.12.1.1/24 dev enp6s0f0

ip -netns tg addr add 12:2::1/64 dev enp6s0f1
ip -netns tg addr add 10.12.2.1/24 dev enp6s0f1

ip -netns tg -6 neigh add 12:1::2 lladdr 00:00:00:00:02:00 dev enp6s0f0
ip -netns tg -6 neigh add fc00::2 lladdr 00:00:00:00:02:00 dev enp6s0f0
ip -netns tg -6 neigh add fc02::2 lladdr 00:00:00:00:02:00 dev enp6s0f0

ip -netns tg -6 neigh add 12:2::2 lladdr 00:00:00:00:02:01 dev enp6s0f1

read -r -d '' tg_env <<-EOF
	# Everything that is private to the bash process that will be launch
	# mount the bpf filesystem.
	# Note: childs of the launching (parent) bash can access this instance
	# of the bpf filesystem. If you need to get access to the bpf filesystem
	# (where maps are available), you need to use nsenter with -m and -t
	# that points to the pid of the parent process (launching bash).
	# mount -t bpf bpf /sys/fs/bpf/
	# mount -t tracefs nodev /sys/kernel/tracing

	# It allows to load maps with many entries without failing
	# ulimit -l unlimited

	/bin/bash
EOF

####################
#### Node: SUT #####
####################
echo -e "\nNode: SUT"
ip netns exec sut sysctl -w net.ipv4.ip_forward=1
ip netns exec sut sysctl -w net.ipv6.conf.all.forwarding=1

ip -netns sut link set dev lo up

ip -netns sut link set dev enp6s0f0 address 00:00:00:00:02:00
ip -netns sut link set dev enp6s0f1 address 00:00:00:00:02:01

ip -netns sut link set dev enp6s0f0 up
ip -netns sut link set dev enp6s0f1 up

# Sink interface (dummy)
ip -netns sut link set dev cl0 up
ip -netns sut addr add cafe::1/64 dev cl0

ip -netns sut addr add 12:1::2/64 dev enp6s0f0
ip -netns sut addr add fc01::2/64 dev enp6s0f0
ip -netns sut addr add fc01::3/64 dev enp6s0f0
ip -netns sut addr add fc02::2/64 dev enp6s0f0
ip -netns sut addr add 10.12.1.2/24 dev enp6s0f0

ip -netns sut addr add 12:2::2/64 dev enp6s0f1
ip -netns sut addr add 10.12.2.2/24 dev enp6s0f1

ip -netns sut -6 neigh add 12:1::1 lladdr 00:00:00:00:01:00 dev enp6s0f0
ip -netns sut -6 neigh add fc00::1 lladdr 00:00:00:00:01:00 dev enp6s0f0
ip -netns sut -6 neigh add fc02::1 lladdr 00:00:00:00:01:00 dev enp6s0f0

ip -netns sut -6 neigh add 12:2::1 lladdr 00:00:00:00:01:01 dev enp6s0f1

#export HIKECC="../hike-tools/hikecc.sh"

read -r -d '' sut_env <<-EOF
	# Everything that is private to the bash process that will be launch
	# mount the bpf filesystem.
	# Note: childs of the launching (parent) bash can access this instance
	# of the bpf filesystem. If you need to get access to the bpf filesystem
	# (where maps are available), you need to use nsenter with -m and -t
	# that points to the pid of the parent process (launching bash).

	/bin/bash
EOF

###

####################
#### Node: CLT #####
####################
echo -e "\nNode: CLT"
ip netns exec clt sysctl -w net.ipv4.ip_forward=1
ip netns exec clt sysctl -w net.ipv6.conf.all.forwarding=1

ip -netns clt link set dev lo up
ip -netns clt link set dev veth0 up

ip -netns clt addr add cafe::2/64 dev veth0

read -r -d '' clt_env <<-EOF
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
	# Attach the (pinned) raw_pass program to netdev veth0 on the
	# XDP hook.
	bpftool net attach xdpdrv 				\
		pinned /sys/fs/bpf/progs/rawpass/xdp_pass	\
                dev veth0

	/bin/bash
EOF

###

## Create a new tmux session
sleep 1

tmux new-session -d -s $TMUX -n MAIN bash
tmux new-window -t $TMUX -n MAPS bash
tmux new-window -t $TMUX -n TG1 ip netns exec tg bash -c "${tg_env}"
tmux new-window -t $TMUX -n TG2 ip netns exec tg bash 
tmux new-window -t $TMUX -n SUT ip netns exec sut bash -c "${sut_env}"
tmux new-window -t $TMUX -n SUTDA ip netns exec sut bash -c "python eclatd.py"
tmux new-window -t $TMUX -n CLT ip netns exec clt bash -c "${clt_env}"

#tmux select-window -t :4

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:SUTDA | grep 'Server started.')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "making sure that the eCLAT daemon is running..."
done

tmux send-keys -t $TMUX:SUT "scripts/run-eclat.sh test/eclat_scripts/tstamp_twamp.eclat enp6s0f0" C-m

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:SUT | grep 'status: "OK"')
  sleep 2
  #tmux send-keys -t $TMUX:TG2 $OUTPUT
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "registering HIKe eBPF Programs and eCLAT Chains..."
done

tmux send-keys -t $TMUX:SUT "clear" C-m
tmux send-keys -t $TMUX:MAIN "scripts/enter-namespace-xdp-raw-pass.sh" C-m
tmux send-keys -t $TMUX:MAPS "scripts/enter-namespace-watchmap.sh" C-m
tmux send-keys -t $TMUX:CLT "tcpdump -i veth0" C-m
tmux send-keys -t $TMUX:TG1 "ping -i 0.01 fc01::2"
tmux send-keys -t $TMUX:TG2 "ping -i 0.5 fc01::3" 

tmux select-window -t $TMUX:TG2
tmux set-option -g mouse on
tmux attach -t $TMUX
