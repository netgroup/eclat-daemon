#!/bin/bash

source scripts/copy-package-mynet.sh

python clean.py
python eclat.py --load test/eclat_scripts/ddos_tb_and_mon_dstonly.eclat --define DEVNAME enp6s0f0 --package test
