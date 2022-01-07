#!/bin/bash

nsenter -t $(ps ax | grep e[c]lat | grep -v '\.eclat'  | awk '{ print $1 }') -m -n -- bash -c "cd /opt/eclat-daemon && /bin/bash"
