# this script is included in other testbed startup scripts
#
# topology:
#
#   +--------------+   +--------------+   +--------------+   +--------------+   +--------------+
#   |      h1      |   |       r2     |   |      r3      |   |      r4      |   |      h5      |
#   |              |   |              |   |              |   |              |   |              |
#   |          i12 +---+ i21      i23 +---+ i32      i34 +---+ i43      i45 +---+ i54          |
#   |              |   |              |   |              |   |              |   |              |
#   |              |   |              |   |              |   |              |   |              |
#   +--------------+   +--------------+   +--------------+   +--------------+   +--------------+
#
# addresses:
# fd00::/8  <-  customers IPv6 networks
# fc00::/8  <-  operator networks and SIDs
#
# 10.0.0.0/8  <-  customers IPv4 networks
#
# h1 i12 fd12::1/64 mac 00:00:00:00:01:02 IPv4 10.12.0.1/24
#
# r2 i21 fd12::2/64 mac 00:00:00:00:02:01 IPv4 10.12.0.2/24
# r2 i23 fc23::1/64 mac 00:00:00:00:02:03
#
# r3 i32 fc23::2/64 mac 00:00:00:00:03:02
# r3 i34 fd34::1/64 mac 00:00:00:00:03:04
#
# r4 i43 fc34::2/64 mac 00:00:00:00:04:03
# r4 i45 fd45::1/64 mac 00:00:00:00:04:05 IPv4 10.45.0.1/24
#
# h5 i54 fd45::2/64 mac 00:00:00:00:05:04 IPv4 10.45.0.2/24
#
# SIDs:
# fc00::2:dt46   Decap (v4v6) and table lookup on node R2
# fc00::3:e      Endpoint function on node R3
# fc00::4:dt46   Decap (v4v6) and table lookup on node R4
#

TMUX=ebpf
KENCAP=true

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

#tmux new-session -d -s $TMUX -n MAIN bash -c "python eclatd.py"
#
#while :
#do
#  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:MAIN | grep 'Server started.')
#  sleep 2
#  if [[ $OUTPUT ]] ; then
#    break
#  fi
#  echo "making sure that the eCLAT daemon is running..."
#done
#
##clones the packages repositories if needed
##python eclat.py --fetch $ECLAT_SCRIPT --define DEVNAME i12 --package test
#python eclat.py fetch $ECLAT_SCRIPT
#
#if [ $? -ne 0 ] ; then
#  echo "Error cloning the packages"
#  python eclat.py quit
#  exit 1
#fi
#
#echo "Cloned the packages if needed"
#python eclat.py quit

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

# Clean up previous network namespaces
ip -all netns delete

ip netns add h1
ip netns add r2
ip netns add r3
ip netns add r4
ip netns add h5

ip -netns h1 link add i12 type veth peer name i21 netns r2
ip -netns r2 link add i23 type veth peer name i32 netns r3
ip -netns r3 link add i34 type veth peer name i43 netns r4
ip -netns r4 link add i45 type veth peer name i54 netns h5

###################
#### Node: h1 #####
###################
NODE=h1
echo -e "\nNode: $NODE"

ip -netns $NODE link set dev i12 address 00:00:00:00:01:02

ip -netns $NODE link set dev lo up
ip -netns $NODE link set dev i12 up

ip -netns $NODE addr add fd12::1/64 dev i12
ip -netns $NODE addr add 10.12.0.1/24 dev i12

ip -netns $NODE -6 neigh add fd12::2   lladdr 00:00:00:00:02:01 dev i12
ip -netns $NODE -4 neigh add 10.12.0.2 lladdr 00:00:00:00:02:01 dev i12

ip -netns $NODE -6 route add default via fd12::2   dev i12
ip -netns $NODE -4 route add default via 10.12.0.2 dev i12

read -r -d '' ${NODE}_env <<-EOF
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

###################
#### Node: r2 #####
###################
NODE=r2
TID=100
echo -e "\nNode: $NODE"

ip -netns $NODE link set dev i21 address 00:00:00:00:02:01
ip -netns $NODE link set dev i23 address 00:00:00:00:02:03

ip -netns $NODE link set dev lo up
ip -netns $NODE link set dev i21 up
ip -netns $NODE link set dev i23 up

ip netns exec $NODE sh -c "echo 1 > /proc/sys/net/vrf/strict_mode"
ip -netns $NODE link add vrf-$TID type vrf table $TID
ip -netns $NODE link set vrf-$TID up
ip -netns $NODE link set i21 master vrf-$TID

ip -netns $NODE addr add fd12::2/64 dev i21
ip -netns $NODE addr add 10.12.0.2/24 dev i21
ip -netns $NODE addr add fc23::1/64 dev i23

ip -netns $NODE -6 neigh add fc12::1   lladdr 00:00:00:00:01:02 dev i21
ip -netns $NODE -6 neigh add fc23::2   lladdr 00:00:00:00:03:02 dev i23
ip -netns $NODE -4 neigh add 10.12.0.1 lladdr 00:00:00:00:01:02 dev i21

ip -netns $NODE -6 route add default via fc23::2 dev i23

if [ $KENCAP = true ]
then
  ip -netns $NODE -6 route add fd45::/64 encap seg6 mode encap segs fc00::4:d46 dev i23
  ip -netns $NODE -4 route add 10.45.0.0/24 encap seg6 mode encap segs fc00::3:e,fc00::4:d46 dev i23
fi

ip -netns $NODE -6 route add fc00::2:d46 encap seg6local action End.DT46 vrftable $TID dev i21

read -r -d '' ${NODE}_env <<-EOF
	echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

	/bin/bash
EOF

###################
#### Node: r3 #####
###################
NODE=r3
echo -e "\nNode: $NODE"

ip -netns $NODE link set dev i32 address 00:00:00:00:03:02
ip -netns $NODE link set dev i34 address 00:00:00:00:03:04

ip -netns $NODE link set dev lo up
ip -netns $NODE link set dev i32 up
ip -netns $NODE link set dev i34 up

ip -netns $NODE addr add fc23::2/64 dev i32
ip -netns $NODE addr add fc34::1/64 dev i34

ip -netns $NODE -6 neigh add fc23::1 lladdr 00:00:00:00:02:03 dev i32
ip -netns $NODE -6 neigh add fc34::2 lladdr 00:00:00:00:04:03 dev i34

ip -netns $NODE -6 route add fc00::2:0/112 via fc23::1 dev i32
ip -netns $NODE -6 route add fc00::4:0/112 via fc34::2 dev i34

ip -netns $NODE -6 route add fc00::3:e encap seg6local action End dev i34

read -r -d '' ${NODE}_env <<-EOF
	echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

	/bin/bash
EOF

###################
#### Node: r4 #####
###################
NODE=r4
TID=100
echo -e "\nNode: $NODE"

ip -netns $NODE link set dev i43 address 00:00:00:00:04:03
ip -netns $NODE link set dev i45 address 00:00:00:00:04:05

ip -netns $NODE link set dev lo up
ip -netns $NODE link set dev i43 up
ip -netns $NODE link set dev i45 up

ip netns exec $NODE sh -c "echo 1 > /proc/sys/net/vrf/strict_mode"
ip -netns $NODE link add vrf-$TID type vrf table $TID
ip -netns $NODE link set vrf-$TID up
ip -netns $NODE link set i45 master vrf-$TID

ip -netns $NODE addr add fc34::2/64 dev i43
ip -netns $NODE addr add fd45::1/64 dev i45
ip -netns $NODE addr add 10.45.0.1/24 dev i45

ip -netns $NODE -6 neigh add fc34::1 lladdr 00:00:00:00:03:04 dev i43
ip -netns $NODE -6 neigh add fd45::2 lladdr 00:00:00:00:05:04 dev i45

ip -netns $NODE -6 route add default via fc34::1 dev i43

if [ $KENCAP = true ]
then
  ip -netns $NODE -6 route add fd12::/64 encap seg6 mode encap segs fc00::2:d46 dev i43
  ip -netns $NODE -4 route add 10.12.0.0/24 encap seg6 mode encap segs fc00::3:e,fc00::2:d46 dev i43
fi

ip -netns $NODE -6 route add fc00::4:d46 encap seg6local action End.DT46 vrftable $TID dev i45

read -r -d '' ${NODE}_env <<-EOF
        echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

        /bin/bash
EOF

###################
#### Node: h5 #####
###################
NODE=h5
echo -e "\nNode: $NODE"

ip -netns $NODE link set dev i54 address 00:00:00:00:05:04

ip -netns $NODE link set dev lo up
ip -netns $NODE link set dev i54 up

ip -netns $NODE addr add fd45::2/64 dev i54
ip -netns $NODE addr add 10.45.0.2/24 dev i54

ip -netns $NODE -6 neigh add fd45::1   lladdr 00:00:00:00:04:05 dev i54
ip -netns $NODE -4 neigh add 10.45.0.1 lladdr 00:00:00:00:04:05 dev i54

ip -netns $NODE -6 route add default via fd45::1   dev i54
ip -netns $NODE -4 route add default via 10.45.0.1 dev i54

read -r -d '' ${NODE}_env <<-EOF
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


## Create a new tmux session
sleep 1

tmux new-session -d -s $TMUX -n MAIN bash
tmux new-window -t $TMUX -n MAPS bash
tmux new-window -t $TMUX -n DEBUG bash
tmux new-window -t $TMUX -n H1 ip netns exec h1 bash
tmux new-window -t $TMUX -n R2 ip netns exec r2 bash -c "${r2_env}"
#tmux new-window -t $TMUX -n R2DA ip netns exec r2 bash -c "python eclatd.py"
#
#while :
#do
#  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R2DA | grep 'Server started.')
#  sleep 2
#  if [[ $OUTPUT ]] ; then
#    break
#  fi
#  echo "making sure that the eCLAT daemon is running in R2..."
#done
#tmux send-keys -t $TMUX:R2 "scripts/run-eclat.sh $ECLAT_SCRIPT i21" C-m
#
#while :
#do
#  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R2 | grep 'status: OK')
#  sleep 2
#  if [[ $OUTPUT ]] ; then
#    break
#  fi
#  echo "waiting for the completion of client start script in R2..."
#done


tmux send-keys -t $TMUX:DEBUG "scripts/enter-namespace-debug-no-vm.sh" C-m

tmux new-window -t $TMUX -n R3 ip netns exec r3 bash -c "${r3_env}"
#tmux new-window -t $TMUX -n R3DA ip netns exec r3 bash -c "python eclatd.py"
tmux new-window -t $TMUX -n R4 ip netns exec r4 bash -c "${r4_env}"
tmux new-window -t $TMUX -n H5 ip netns exec h5 bash
#while :
#do
#  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R3DA | grep 'Server started.')
#  sleep 2
#  if [[ $OUTPUT ]] ; then
#    break
#  fi
#  echo "making sure that the eCLAT daemon is running in R3..."
#done
#
#
#tmux send-keys -t $TMUX:R3 "scripts/run-eclat.sh $ECLAT_SCRIPT i32" C-m

if [[ "$H1_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:H1   "$H1_COMMAND" $CM
if [[ "$MAIN_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:MAIN   "$MAIN_COMMAND" $CM
if [[ "$R4_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:R4   "$R4_COMMAND" $CM

tmux select-window -t $TMUX:H1
tmux set-option -g mouse on
tmux attach -t $TMUX
