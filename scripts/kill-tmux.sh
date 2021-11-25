#!/bin/bash

for i in $(tmux ls | awk '{print $1}' | sed 's/://g'); do tmux kill-session -t ${i}; done

#signle session kill:
#tmux kill-session -t $(ps aux | grep -o "[t]mux attach -t .*" | awk '{print $4}')