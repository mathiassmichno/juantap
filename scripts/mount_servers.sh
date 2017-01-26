for i in `seq -w 00 7`
do
    echo Mounting server $i
    sudo mount -t overlay -o "lowerdir=$HOME/lower,upperdir=$HOME/servers/$i/.upper,workdir=$HOME/servers/$i/.work" overlay "$HOME/servers/$i/server"
done
