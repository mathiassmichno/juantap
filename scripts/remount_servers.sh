for i in `seq -w 00 7`
do
    echo Remounting server $i
    sudo mount -o remount "$HOME/servers/$i/server"
done
