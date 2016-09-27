#!/usr/bin/env bash
if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo or as root"
    exit 1
fi

echo "$1"
echo "$2"

S_PATH=~/servers/"$1"

#scaffold and mount dirs
cp -r ~/servers/skel "$S_PATH"
tree "$S_PATH"
mount -t overlay -o lowerdir=~/lower,upperdir="$S_PATH"/upper,workdir="$S_PATH"/work overlay "$S_PATH"/server
#move match config to server
mv "$2" "$1"/server/serverfiles/csgo/match.json
