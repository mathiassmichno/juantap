import begin
import logging
import os
import subprocess

script_folder="./scripts"

def _run_script(script, args, action_msg):
	logging.info(action_msg)
		try:
			subprocess.run([os.path.join(script_folder, script), *args], shell=True, check=True)
		except CalledProcessError as e:
			logging.error(e)

@begin.subcommand
@begin.logging
def scaffold_servers(num_servers: 'Number of servers to setup' = 8,
		 			 start_num: 'Number used for the first server' = 0,
		 			 servers_folder: 'Where to place new servers' = './servers'):
	for i in range(start_num, start_num + num_servers):
		os.makedirs(os.path.join(servers_folder, '{:02}'.format(i)))
		os.makedirs(os.path.join(servers_folder, '.{:02}'.format(i), 'upper'))
		os.makedirs(os.path.join(servers_folder, '.{:02}'.format(i), 'work'))

@begin.subcommand
@begin.logging
def mount_servers(num_servers: 'Number of servers to setup' = 8,
		 		  start_num: 'Number used for the first server' = 0,
		 		  root_server: 'Path to the root server' = './root_server',
		 		  servers_folder: 'Where to place new servers' = './servers'):
	for i in range(start_num, start_num + num_servers):
		_run_script(script="mount_server.sh",
					args=['{:02}'.format(i), root_server, servers_folder],
					action_msg="Mounting server {:02}".format(i))

@begin.subcommand
@begin.logging
def unmount_servers(num_servers: 'Number of servers to setup' = 8,
		 			 start_num: 'Number used for the first server' = 0,
		 			 servers_folder: 'Where to place new servers' = './servers'):
	for i in range(start_num, start_num + num_servers):
		_run_script(script="unmount_server.sh",
					args=['{:02}'.format(i), servers_folder],
					action_msg="Unmounting server {:02}".format(i))

@begin.subcommand
@begin.logging
def remount_servers(num_servers: 'Number of servers to setup' = 8,
		 			start_num: 'Number used for the first server' = 0,
		 			servers_folder: 'Where to place new servers' = './servers'):
	for i in range(start_num, start_num + num_servers):
		_run_script(script="remount_server.sh",
					args=['{:02}'.format(i), servers_folder],
					action_msg="Remounting server {:02}".format(i))
		
@begin.start
@begin.logging
def main(num_servers: 'Number of servers to setup' = 8,
		 start_num: 'Number used for the first server' = 0,
		 root_server: 'Path to the root server' = '.',
		 servers_folder: 'Where to place new servers' = './servers'):
	scaffold_servers(num_servers=num_servers, start_num=start_num, servers_folder=servers_folder)