#!/bin/bash

nsenter -t $(ps ax | grep e[c]lat | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && watch python process_maps.py"
