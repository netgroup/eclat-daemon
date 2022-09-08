# used to setup a basic environment for development
# with no testbed
# it creates 3 TMUX window
# it executes the eclat daemon in the DAEMON window, but it does not execute the client
#
# topology: none
#


MAPS_COMMAND="scripts/enter-namespace-watchmap.sh"
MAPS_EXEC=YES

CLT_COMMAND="tcpdump -i veth0"
CLT_EXEC=NO

TG1_COMMAND="tcpreplay -i enp6s0f0 hike/testbed/pkts/pkt_ipv6_udp.pcap"
TG1_EXEC=NO

TG2_COMMAND="ping -i 5 fc01::3"
TG2_EXEC=NO

SUT_COMMAND="scripts/run-eclat.sh $ECLAT_SCRIPT $SUT_DEV0"
SUT_EXEC=NO

TMUX=ebpf
IPP=ip



#build the hike vm bpf.c files if needed
scripts/initial_setup.sh

echo "Initial setup done (make HIKe)"

# Kill tmux previous session
tmux kill-session -t $TMUX 2>/dev/null

#tmux new-session -d -s $TMUX -n DAEMON bash -c "python eclatd.py"
tmux new-session -d -s $TMUX -n CLIENT1 bash
#tmux new-window -t $TMUX -n
tmux new-window -t $TMUX -n CLIENT2 bash
tmux new-window -t $TMUX -n DAEMON bash -c "python eclatd.py"


while :
do
  OUTPUT=$(tmux capture-pane -pJ -S-100 -t $TMUX:DAEMON | grep 'Server started.')
  sleep 2
  if [[ $OUTPUT ]] ; then
    break
  fi
  echo "making sure that the eCLAT daemon is running"
done



sleep 1


tmux select-window -t $TMUX:CLIENT1
tmux set-option -g mouse on
tmux attach -t $TMUX
