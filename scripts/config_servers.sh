#!/bin/bash
for i in `seq -w 00 7`
do
    mv "$HOME/servers/$i/server/serverfiles/csgo/cfg/csgo-server.cfg" "$HOME/servers/$i/server/serverfiles/csgo/cfg/csgo-server-$i.cfg"
    sed -i 's/^hostname.*/hostname\ \"FLAN 5.0 \['"$i"'\]"/' "$HOME/servers/$i/server/serverfiles/csgo/cfg/csgo-server-$i.cfg"
    sed -i 's/^exec.*/exec\ csgo-server-'"$i"'.cfg/' "$HOME/servers/$i/server/serverfiles/csgo/cfg/server.cfg"
    sed -i 's/^servicename.*/servicename=\"csgo-server-'"$i"'\"/' "$HOME/servers/$i/server/csgoserver"
    sed -i 's/^port.*/port=\"'"$(($i+27015))"'\"/' "$HOME/servers/$i/server/csgoserver"
    sed -i 's/^sourcetvport.*/sourcetvport=\"'"$(($i+27115))"'\"/' "$HOME/servers/$i/server/csgoserver"
    sed -i 's/^clientport.*/clientport=\"'"$(($i+27215))"'\"/' "$HOME/servers/$i/server/csgoserver"
done
