#!/bin/bash
# usage:   run-eclat.sh SCRIPT DEVICE
# example: run-eclat.sh test/eclat_scripts/ddos_tb_met.eclat enp6s0f0

# all packages are automatically cloned from git if not present

#python clean.py
python eclat.py load $1 --define DEVNAME $2 
