#!/bin/bash

# Before running this script,
# put a file named github_rsa with your private key
# in the folder /opt/eclat-daemon/scripts/temp_credentials/

# moreover, to update your global git user.name and user.email
# this script optionally takes as input your email address and user name
#
# copy-credential you@example.com "Your Name"

[ -d "/root/.ssh" ] || mkdir /root/.ssh
cp scripts/temp_credentials/config /root/.ssh
cp scripts/temp_credentials/github_rsa /root/.ssh
chmod 600 /root/.ssh/github_rsa

if [ -z "$1" ]
then
      : #echo "git user.email not provided"
else
      git config --global user.email "$1"
fi

if [ -z "$2" ]
then
      : #echo "git user.name not provided"
else
      git config --global user.name "$2"

fi
