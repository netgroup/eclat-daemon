#!/bin/bash

nsenter -t $(ps ax | grep e[c]latd | grep -v '\.eclat'  | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && python stamp_maps.py"
