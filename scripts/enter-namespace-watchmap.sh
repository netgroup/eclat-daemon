#!/bin/bash

nsenter -t $(ps ax | grep e[c]latd | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && watch -n 0.8 python process_maps.py"
