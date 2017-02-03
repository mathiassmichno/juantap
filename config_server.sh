#!/usr/bin/env bash
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo or as root"
    exit 1
fi

echo "$1"
echo "$2"

S_PATH=~/servers/"$1"

#scaffold and mount dirs
mv "$2" "$1"/server/serverfiles/csgo/match.json
