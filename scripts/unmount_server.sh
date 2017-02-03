#!/bin/bash
if [[ $# -ne 2 ]]; then
    echo "Illegal number of parameters"
    exit 1
fi
SERVER_NO=$1
SERVERS_FOLDER=$2

sudo umount "$SERVERS_FOLDER/$SERVER_NO"
