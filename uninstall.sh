#!/usr/bin/env bash

# cd into folder of this script so we have a known working folder
cd "${0%/*}" || exit

# exit if not root
ROOTUID="0"
if [ "$(id -u)" -ne "$ROOTUID" ] ; then
    echo "This script must be run with root privileges."
    exit 1
fi

EGGFILE="python_mcp3425-1.0-py3.5.egg"
# sudo easy_install -m /usr/local/lib/python3.5/dist-packages/$EGGFILE
sudo rm /usr/local/lib/python3.5/dist-packages/$EGGFILE
sudo rm -r build dist python_mcp3425.egg-info
echo "Uninstalled $EGGFILE"