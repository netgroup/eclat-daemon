# this script is included in other testbed startup scripts
#
# topology:
#
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

SUT_DEV0=enp6s0f0
SUT_DEV1=enp6s0f1

TG_DEV0=enp6s0f0
TG_DEV1=enp6s0f1


#build the hike vm bpf.c files if needed
scripts/initial_setup.sh

echo "Initial setup done (make HIKe)"

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

tmux new-session -d -s $TMUX -n MAIN bash -c "python eclatd.py"

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:MAIN | grep 'Server started.')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "making sure that the eCLAT daemon is running (to prefetch the packages)..."
done

#clones the packages repositories if needed
#python eclatd.py &
#sleep 3

python eclat.py fetch $ECLAT_SCRIPT 

if [ $? -ne 0 ] ; then
  echo "Error cloning the packages"
  python eclat.py quit
  exit 1
fi

echo "Cloned the packages if needed"
python eclat.py quit

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

# Clean up previous network namespaces
ip -all netns delete

ip netns add tg
ip netns add sut
ip netns add clt

ip -netns tg link add $TG_DEV0 type veth peer name $SUT_DEV0 netns sut
ip -netns tg link add $TG_DEV1 type veth peer name $SUT_DEV1 netns sut

ip -netns sut link add cl0 type veth peer name veth0 netns clt

###################
#### Node: TG #####
###################
echo -e "\nNode: TG"

ip -netns tg link set dev lo up

ip -netns tg link set dev $TG_DEV0 address 00:00:00:00:01:00
ip -netns tg link set dev $TG_DEV1 address 00:00:00:00:01:01

ip -netns tg link set dev $TG_DEV0 up
ip -netns tg link set dev $TG_DEV1 up

ip -netns tg addr add 12:1::1/64 dev $TG_DEV0
ip -netns tg addr add fc01::1/64 dev $TG_DEV0
ip -netns tg addr add fc02::1/64 dev $TG_DEV0
ip -netns tg addr add 10.12.1.1/24 dev $TG_DEV0

ip -netns tg addr add 12:2::1/64 dev $TG_DEV1
ip -netns tg addr add 10.12.2.1/24 dev $TG_DEV1

ip -netns tg -6 neigh add 12:1::2 lladdr 00:00:00:00:02:00 dev $TG_DEV0
ip -netns tg -6 neigh add fc00::2 lladdr 00:00:00:00:02:00 dev $TG_DEV0
ip -netns tg -6 neigh add fc02::2 lladdr 00:00:00:00:02:00 dev $TG_DEV0

ip -netns tg -6 neigh add 12:2::2 lladdr 00:00:00:00:02:01 dev $TG_DEV1

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

ip -netns sut link set dev $SUT_DEV0 address 00:00:00:00:02:00
ip -netns sut link set dev $SUT_DEV1 address 00:00:00:00:02:01

ip -netns sut link set dev $SUT_DEV0 up
ip -netns sut link set dev $SUT_DEV1 up

# Sink interface (dummy)
ip -netns sut link set dev cl0 up
ip -netns sut addr add cafe::1/64 dev cl0

ip -netns sut addr add 12:1::2/64 dev $SUT_DEV0
ip -netns sut addr add fc01::2/64 dev $SUT_DEV0
ip -netns sut addr add fc01::3/64 dev $SUT_DEV0
ip -netns sut addr add fc02::2/64 dev $SUT_DEV0
ip -netns sut addr add 10.12.1.2/24 dev $SUT_DEV0

ip -netns sut addr add 12:2::2/64 dev $SUT_DEV1
ip -netns sut addr add 10.12.2.2/24 dev $SUT_DEV1

ip -netns sut -6 neigh add 12:1::1 lladdr 00:00:00:00:01:00 dev $SUT_DEV0
ip -netns sut -6 neigh add fc00::1 lladdr 00:00:00:00:01:00 dev $SUT_DEV0
ip -netns sut -6 neigh add fc02::1 lladdr 00:00:00:00:01:00 dev $SUT_DEV0

ip -netns sut -6 neigh add 12:2::1 lladdr 00:00:00:00:01:01 dev $SUT_DEV1

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
tmux new-window -t $TMUX -n DEBUG bash
tmux new-window -t $TMUX -n TG1 ip netns exec tg bash -c "${tg_env}"
tmux new-window -t $TMUX -n TG2 ip netns exec tg bash 
tmux new-window -t $TMUX -n SUT ip netns exec sut bash -c "${sut_env}"
tmux new-window -t $TMUX -n SUT2 ip netns exec sut bash 
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

tmux send-keys -t $TMUX:SUT "scripts/run-eclat.sh $ECLAT_SCRIPT $SUT_DEV0" C-m


while :
do
  OUTPUT=$(tmux capture-pane -pJ -S -100 -t $TMUX:SUT | grep -E 'status: OK|status: ERROR')
  sleep 2
  #tmux send-keys -t $TMUX:TG2 $OUTPUT
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "registering HIKe eBPF Programs and eCLAT Chains..."
done

if grep -q "Offending command is" <<< "$OUTPUT"; then
	echo "ERROR !!!"
	echo "$OUTPUT"
	exit 1
fi

if grep -q "Compilation failed" <<< "$OUTPUT"; then
	echo "ERROR !!!"
	echo "$OUTPUT"
	exit 1
fi

if grep -q "debug_error_string" <<< "$OUTPUT"; then
	echo "ERROR !!!"
	echo "$OUTPUT"
	exit 1
fi

tmux send-keys -t $TMUX:SUT   "clear" C-m

sleep 2

#the following is needed to enable raw-pass for l2-redirect in the SUT
tmux send-keys -t $TMUX:MAIN  "scripts/enter-namespace-xdp-raw-pass.sh" C-m

sleep 1

if [[ "$DEBUG_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:DEBUG "$DEBUG_COMMAND" $CM

if [[ "$MAPS_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:MAPS  "$MAPS_COMMAND" $CM

if [[ "$CLT_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:CLT   "$CLT_COMMAND" $CM

if [[ "$TG1_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:TG1   "$TG1_COMMAND" $CM

if [[ "$TG2_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:TG2   "$TG2_COMMAND" $CM

if [[ "$MAIN_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:MAIN   "$MAIN_COMMAND" $CM

if [[ "$SUT_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:SUT   "$SUT_COMMAND" $CM

if [[ "$SUT2_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:SUT2   "$SUT2_COMMAND" $CM

tmux select-window -t $TMUX:TG2
tmux set-option -g mouse on
tmux attach -t $TMUX
