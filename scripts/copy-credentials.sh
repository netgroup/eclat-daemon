#!/bin/bash

[ -d "/root/.ssh" ] || mkdir /root/.ssh
cp scripts/temp_credentials/config /root/.ssh
cp scripts/temp_credentials/github_rsa /root/.ssh
chmod 600 /root/.ssh/github_rsa

