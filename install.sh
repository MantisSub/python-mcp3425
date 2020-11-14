#!/usr/bin/env bash

# cd into folder of this script so we have a known working folder
cd "${0%/*}" || exit

# exit if not root
ROOTUID="0"
if [ "$(id -u)" -ne "$ROOTUID" ] ; then
    echo "This script must be run with root privileges."
    exit 1
fi

sudo python3 setup.py install