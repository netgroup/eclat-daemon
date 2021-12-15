#!/bin/bash

rm -rf hike_v3
git clone git@github.com:netgroup/hike_v3.git
cd hike_v3
git checkout stefano2
git submodule update --init --recursive

