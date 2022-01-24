#!/bin/bash
# usage:   run-eclat.sh SCRIPT DEVICE
# example: run-eclat.sh test/eclat_scripts/ddos_tb_met.eclat enp6s0f0 

#source scripts/copy-package-mynet.sh

# all packages are automatically cloned from git if not present
# but it is still needed to copy the default package 
python copy_hike_packages.py

#python clean.py
python eclat.py --load $1 --define DEVNAME $2 --package test
