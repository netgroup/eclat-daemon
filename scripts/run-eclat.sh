#!/bin/bash
# usage:   run-eclat SCRIPT DEVICE
# example: run-eclat test/eclat_scripts/ddos_tb_met.eclat enp6s0f0 

source scripts/copy-package-mynet.sh

python clean.py
python eclat.py --load $1 --define DEVNAME $2 --package test
