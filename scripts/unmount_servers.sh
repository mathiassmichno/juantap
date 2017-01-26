for i in `seq -w 00 7`
do
    echo Unmounting server $i
    sudo umount "$HOME/servers/$i/server"
done
