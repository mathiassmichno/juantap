
# Juantap 

## Get started

1. Install juantap with `pip3 install git+https://github.com/mathiassmichno/juantap`
2. Configure juantap as wanted: `juantap config -e`
3. Create the file `~/gslts.txt` with the Game Server Login tokens in.
   * One token per line per game server, so each instance have a token
4. Setup juantap root and install LGSM: `juantap root setup --install` (it can take some time)
   * LGSM requires the following dependencies:
       * tmux
       * wget
       * ca-certificates
       * file
       * bsdmainutils
       * util-linux
       * python
       * bzip2
       * gzip
       * unzip
       * binutils
       * lib32gcc1
       * libstdc++6:i386
   * Do not run it in tmux, LGSM run its scripts in tmux, and can't handle nested tmux
   * If it will not install, try to run `~/rootserver/csgoserver install` to install LGSM manually
      * Thís will also tell which dependencies are missing, and offer to install them automatically
   * `juantap root setup --install` returns, without any errors, if any dependencies are missing
      * It is first when you try to run `juantap instances cmd start`, that it tells the dependencies are missing
5. Copy common settings to the root server: `juantap root config -c`
6. Scaffold instances: `juantap instances scaffold`
7. Mount the instances: `juantap instances mount`
8. Copy the settings to the instances: `juantap instances setup`	
9. Start the CS servers: `juantap instances cmd start`

## Usage
* To control all instances: `juantap instances cmd xx`
   * For instance:  `juantap instances cmd stop`
* To control a single instance: `juantap instances -i yy cmd xx`
   * For instance: `juantap instances -i 01 cmd details`

## juantap CMD commands
```
start         st   | Start the server.
stop          sp   | Stop the server.
restart       r    | Restart the server.
monitor       m    | Check server status and restart if crashed.
test-alert    ta   | Send a test alert.
details       dt   | Display server information.
postdetails   pd   | Post details to hastebin (removing passwords).
update-lgsm   ul   | Check and apply any LinuxGSM updates.
update        u    | Check and apply any server updates.
force-update  fu   | Apply server updates bypassing check.
validate      v    | Validate server files with SteamCMD.
backup        b    | Create backup archives of the server.
console       c    | Access server console.
debug         d    | Start server directly in your terminal.
fastdl        fd   | Build a FastDL directory.
mods-install  mi   | View and install available mods/addons.
mods-remove   mr   | View and remove an installed mod/addon.
mods-update   mu   | Update installed mods/addons.
install       i    | Install the server.
auto-install  ai   | Install the server without prompts.
developer     dev  | Enable developer Mode.

```

