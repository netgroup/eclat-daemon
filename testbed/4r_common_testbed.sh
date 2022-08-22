# this script is included in other testbed startup scripts
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


TMUX=ebpf

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
  echo "making sure that the eCLAT daemon is running..."
done

#clones the packages repositories if needed
#python eclat.py --fetch $ECLAT_SCRIPT --define DEVNAME i12 --package test
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

ip netns add r1
ip netns add r2
ip netns add r3
ip netns add r4

ip -netns r1 link add i12 type veth peer name i21 netns r2
ip -netns r2 link add i23 type veth peer name i32 netns r3
ip -netns r3 link add i34 type veth peer name i43 netns r4

###################
#### Node: r1 #####
###################
echo -e "\nNode: r1"

ip -netns r1 link set dev i12 address 00:00:00:00:01:02

ip -netns r1 link set dev lo up
ip -netns r1 link set dev i12 up

ip -netns r1 addr add fc12::1/64 dev i12
ip -netns r1 addr add 10.12.0.1/24 dev i12

ip -netns r1 -6 neigh add fc12::2 lladdr 00:00:00:00:02:01 dev i12

ip -netns r1 route add 10.23.0.0/24 via 10.12.0.2
ip -netns r1 route add 10.34.0.0/24 via 10.12.0.2

ip -netns r1 -6 route add fc23::/64 via fc12::2
ip -netns r1 -6 route add fc34::/64 via fc12::2

read -r -d '' r1_env <<-EOF
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
echo -e "\nNode: r2"

ip -netns r2 link set dev i21 address 00:00:00:00:02:01
ip -netns r2 link set dev i23 address 00:00:00:00:02:03

ip -netns r2 link set dev lo up
ip -netns r2 link set dev i21 up
ip -netns r2 link set dev i23 up

ip -netns r2 addr add fc12::2/64 dev i21
ip -netns r2 addr add 10.12.0.2/24 dev i21
ip -netns r2 addr add fc23::1/64 dev i23
ip -netns r2 addr add 10.23.0.1/24 dev i23

ip -netns r2 -6 neigh add fc12::1 lladdr 00:00:00:00:01:02 dev i21
ip -netns r2 -6 neigh add fc23::2 lladdr 00:00:00:00:03:02 dev i23

ip -netns r2 route add 10.34.0.0/24 via 10.23.0.2

ip -netns r2 -6 route add fc34::/64 via fc23::2

read -r -d '' r2_env <<-EOF
	echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

	/bin/bash
EOF

###################
#### Node: r3 #####
###################
echo -e "\nNode: r3"

ip -netns r3 link set dev i32 address 00:00:00:00:03:02
ip -netns r3 link set dev i34 address 00:00:00:00:03:04

ip -netns r3 link set dev lo up
ip -netns r3 link set dev i32 up
ip -netns r3 link set dev i34 up

ip -netns r3 addr add fc23::2/64 dev i32
ip -netns r3 addr add 10.23.0.2/24 dev i32
ip -netns r3 addr add fc34::1/64 dev i34
ip -netns r3 addr add 10.34.0.1/24 dev i34

ip -netns r3 -6 neigh add fc23::1 lladdr 00:00:00:00:02:03 dev i32
ip -netns r3 -6 neigh add fc34::2 lladdr 00:00:00:00:04:03 dev i34

ip -netns r3 route add 10.12.0.0/24 via 10.23.0.1

ip -netns r3 -6 route add fc12::/64 via fc23::1

read -r -d '' r3_env <<-EOF
	echo 1 > /proc/sys/net/ipv6/conf/all/forwarding

	/bin/bash
EOF

###################
#### Node: r4 #####
###################
echo -e "\nNode: r4"

ip -netns r4 link set dev i43 address 00:00:00:00:04:03

ip -netns r4 link set dev lo up
ip -netns r4 link set dev i43 up

ip -netns r4 addr add fc34::2/64 dev i43
ip -netns r4 addr add 10.34.0.2/24 dev i43

ip -netns r4 -6 neigh add fc34::1 lladdr 00:00:00:00:03:04 dev i43

ip -netns r4 route add 10.12.0.0/24 via 10.34.0.1
ip -netns r4 route add 10.23.0.0/24 via 10.34.0.1

ip -netns r4 -6 route add fc12::/64 via fc34::1
ip -netns r4 -6 route add fc23::/64 via fc34::1


## Create a new tmux session
sleep 1

tmux new-session -d -s $TMUX -n MAIN bash
tmux new-window -t $TMUX -n MAPS bash
tmux new-window -t $TMUX -n DEBUG bash
tmux new-window -t $TMUX -n R1 ip netns exec r1 bash
tmux new-window -t $TMUX -n R2 ip netns exec r2 bash -c "${r2_env}"
tmux new-window -t $TMUX -n R2DA ip netns exec r2 bash -c "python eclatd.py"

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R2DA | grep 'Server started.')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "making sure that the eCLAT daemon is running in R2..."
done
tmux send-keys -t $TMUX:R2 "scripts/run-eclat.sh $ECLAT_SCRIPT i21" C-m

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R2 | grep 'status: OK')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "waiting for the completion of client start script in R2..."
done


tmux send-keys -t $TMUX:DEBUG "scripts/enter-namespace-debug-no-vm.sh" C-m

tmux new-window -t $TMUX -n R3 ip netns exec r3 bash -c "${r3_env}"
tmux new-window -t $TMUX -n R3DA ip netns exec r3 bash -c "python eclatd.py"
tmux new-window -t $TMUX -n R4 ip netns exec r4 bash

while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:R3DA | grep 'Server started.')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "making sure that the eCLAT daemon is running in R3..."
done


tmux send-keys -t $TMUX:R3 "scripts/run-eclat.sh $ECLAT_SCRIPT i32" C-m

if [[ "$R1_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:R1   "$R1_COMMAND" $CM
if [[ "$MAIN_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:MAIN   "$MAIN_COMMAND" $CM
if [[ "$R4_EXEC" == "YES" ]] ; then CM="C-m" ; else CM="" ; fi
tmux send-keys -t $TMUX:R4   "$R4_COMMAND" $CM

tmux select-window -t $TMUX:R1
tmux set-option -g mouse on
tmux attach -t $TMUX
