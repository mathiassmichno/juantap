echo "Unmounting servers:"
$HOME/unmount_servers.sh
echo "Delete servers"
rm -rf $HOME/servers/0*
echo "Scaffold new servers"
$HOME/scaffold_servers.sh
echo "Mount server overlayfs"
$HOME/mount_servers.sh
echo "Configure servers"
$HOME/config_servers.sh
echo "Hard reset done..."

