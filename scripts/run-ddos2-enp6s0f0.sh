#!/bin/bash

python clean.py
#python eclat.py --load test/eclat_scripts/ddos2.eclat --define DEVNAME enp6s0f0 --package test
python eclat.py load test/eclat_scripts/ddos2.eclat --define DEVNAME enp6s0f0