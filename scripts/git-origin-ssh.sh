#!/bin/bash

url=$(git remote -v | awk 'NR==1{ print $2 }')
ssh_url="git@github.com:${url:19}"
git remote set-url origin $ssh_url