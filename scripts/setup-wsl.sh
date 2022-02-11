#!/bin/bash

cd ..
rm -rf eclat-daemon

#git clone git@github.com:netgroup/eclat-daemon.git
git clone https://github.com/netgroup/eclat-daemon.git
cd eclat-daemon
git checkout main
#mkdir components/programs/mynet
mkdir components/loaders
cp -r develop/temp-util/basic/ components/loaders/basic

#on windows/WSL the following commands cannot be executed on
#the windows host, they must be executed inside the wsl container
#otherwise the symbolic links does not work
#as a workaround, we use a script in eclat-daemon to delete and
#clone again

git clone https://github.com/netgroup/hike-public
mv hike-public hike_v3
cd hike_v3
git checkout hike4eclat
git submodule update --init --recursive

git clone https://github.com/netgroup/hike-contribs.git contrib-src

