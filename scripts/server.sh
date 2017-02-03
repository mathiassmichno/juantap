#!/bin/bash
# First argument must be server name i.e. 00 - 07
# Second argument is the command to run, (start, stop, restart, console, details, debug)
"$HOME/servers/$1/csgoserver" $2
