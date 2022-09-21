#!/bin/bash

# This script adds the alias 'eclat'
# It is used to fix an old eclat docker
# Recent dockers insert the alias during the build process
#
# After running this script, run source $HOME/.bash_aliases

echo "alias eclat='python eclat.py'" >> $HOME/.bash_aliases
echo ""
echo ">>>>>>>> now you have to execute the following command:"
echo ""
echo "source $HOME/.bash_aliases"
echo ""
echo ">>>>>>>>"
echo ""
