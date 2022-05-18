#!/bin/bash

url=$(git remote -v | awk 'NR==1{ print $2 }')
if [ ${url:0:14} = "git@github.com" ]   # check if origin is already SSH
then
    exit 0
fi
ssh_url="git@github.com:${url:19}"
git remote set-url origin $ssh_url