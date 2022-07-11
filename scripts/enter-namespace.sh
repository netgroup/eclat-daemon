#!/bin/bash

# this script is needed to enter in the pid namespace that has the visibility of the bpf maps
# this script runs a bash that has visibility of the bpf maps managed by eclatd

nsenter -t $(ps ax | grep e[c]latd | grep -v '\.eclat'  | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && /bin/bash"
