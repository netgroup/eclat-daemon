#!/bin/bash
# usage:   run-eclat.sh SCRIPT DEVICE
# example: run-eclat.sh test/eclat_scripts/ddos_tb_met.eclat enp6s0f0 

#2022-01-04
#THIS FILE IS FOR BACKWARD COMPATIBILITY WITH mynet PACKAGE 
#TO BE DELETED IN ONE MONTH...

source scripts/copy-package-mynet.sh
#python copy_hike_packages.py

python clean.py
python eclat.py --load $1 --define DEVNAME $2 --package test