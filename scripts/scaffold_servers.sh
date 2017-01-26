#!/bin/bash
for i in `seq -w 00 7`
do	
    cp -R "$HOME/servers/skel" "$HOME/servers/$i"
done
