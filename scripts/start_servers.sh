for i in $(seq -w 00 $1)
do
    "$HOME/servers/$i/csgoserver" start
done
