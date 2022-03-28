#!/bin/bash

read -r -d '' env2 <<-EOF
	cd /opt/eclat-daemon
    # Python scripts to populate maps
    python stamp_maps.py --once --pkg eip --prog mcd --map eip_mcd_time
	python eip_pt_tts_maps.py --id 21
EOF

read -r -d '' env3 <<-EOF
	cd /opt/eclat-daemon
    # Python scripts to populate maps
    python stamp_maps.py --once --pkg eip --prog mcd --map eip_mcd_time
	python eip_pt_tts_maps.py --id 32
EOF

# compile C program to calculate delta time
cd /opt/eclat-daemon/develop
gcc t2.c -o t2
nsenter -t $(ps ax | grep e[c]latd | grep -v '\.eclat'  | awk 'NR==1{ print $1 }') -m -n -- bash -c "${env2}"
nsenter -t $(ps ax | grep e[c]latd | grep -v '\.eclat'  | awk 'NR==2{ print $1 }') -m -n -- bash -c "${env3}"
