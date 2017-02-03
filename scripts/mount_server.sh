#!/bin/bash
if [[ $# -ne 3 ]]; then
    echo "Illegal number of parameters"
    exit 1
fi
SERVER_NO=$1
ROOT_SERVER=$2
SERVERS_FOLDER=$3

sudo mount -t overlay -o "lowerdir=$ROOT_SERVER,upperdir=$SERVERS_FOLDER/.$SERVER_NO/upper,workdir=$SERVERS_FOLDER/.$SERVER_NO/work" overlay "$SERVERS_FOLDER/$SERVER_NO"
