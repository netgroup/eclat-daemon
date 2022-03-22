#!/bin/bash

nsenter -t $(ps ax | grep e[c]lat |grep -v '\.eclat' | awk 'NR==1{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && cat /sys/kernel/tracing/trace_pipe | grep -v 'HIKe VM debug'"
