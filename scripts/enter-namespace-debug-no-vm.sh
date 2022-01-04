#!/bin/bash

nsenter -t $(ps ax | grep e[c]lat | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && cat /sys/kernel/tracing/trace_pipe | grep -v 'HIKe VM debug'"
