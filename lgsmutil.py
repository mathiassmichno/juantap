import os
import subprocess
import click

script_folder="./scripts"

def _run_script(script, args, action_msg):
    logging.info(action_msg)
    try:
        subprocess.run([os.path.join(script_folder, script), *args], shell=True, check=True)
    except CalledProcessError as e:
        logging.error(e)

class Config(object):
    def __init__(self):
        self.servers = None
        self.start_at = None
        self.outdir = None

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('--num-servers', default=8)
@click.option('--start-at', default=1)
@click.option('--server-dir', type=click.Path(), default='./servers')
@pass_config
def cli(config, num_servers, start_at, server_dir):
    config.num_servers = num_servers
    config.start_at = start_at
    config.server_dir = server_dir

@cli.command()
@pass_config
def scaffold(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        os.makedirs(os.path.join(config.server_dir, '{:02}'.format(i)))
        os.makedirs(os.path.join(config.server_dir, '.{:02}'.format(i), 'upper'))
        os.makedirs(os.path.join(config.server_dir, '.{:02}'.format(i), 'work'))

@cli.command()
@click.option('--root-dir', type=click.Path(), default='./rootserver')
@pass_config
def mount(config, root_dir):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="mount_server.sh",
                    args=['{:02}'.format(i), root_dir, config.server_dir],
                    action_msg="Mounting server {:02}".format(i))

@cli.command()
@pass_config
def unmount(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="unmount_server.sh",
                    args=['{:02}'.format(i), config.server_dir],
                    action_msg="Unmounting server {:02}".format(i))

@cli.command()
@pass_config
def remount(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="remount_server.sh",
                    args=['{:02}'.format(i), config.server_dir],
                    action_msg="Remounting server {:02}".format(i))

