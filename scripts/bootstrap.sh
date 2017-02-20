#!/bin/bash
if [ $USER == 'root' ]; then
	sudo dpkg --add-architecture i386
	sudo apt-get update
	sudo DEBIAN_FRONTEND=noninteractive apt-get -y install  mailutils postfix curl wget file bzip2 gzip unzip bsdmainutils python util-linux tmux lib32gcc1 libstdc++6 libstdc++6:i386

	adduser --gecos "" csgoserver
	cp "$(readlink -f "${BASH_SOURCE[0]}")" "/home/csgoserver/"
	chown csgoserver:csgoserver "/home/csgoserver/bootstrap.sh"
	echo "Change user to csgoserver and run script again from home folder"
	exit 0
fi

cd ${HOME}
wget "https://raw.githubusercontent.com/mathiassmichno/LinuxGSM/master/CounterStrikeGlobalOffensive/.csgoserver_vars"
echo "source .csgoserver_vars" >> ".profile"

mkdir servers
mkdir root_server
cd root_server

wget "https://raw.githubusercontent.com/mathiassmichno/LinuxGSM/master/CounterStrikeGlobalOffensive/csgoserver"
chmod +x ./csgoserver
