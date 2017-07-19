import os
import stat
import subprocess
import click
import requests

script_folder="./scripts"
lgsm_dl_url="https://gameservermanagers.com/dl/linuxgsm.sh"

def _run_script(script="", path=None, args=(), action_msg=""):
    click.echo(action_msg)
    if not path:
        path = os.path.join(script_folder, script)
    try:
        subprocess.run([path, *args], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(e)

class InstanceConfig(object):
    def __init__(self):
        self.servers = None
        self.start_at = None
        self.outdir = None

pass_instance_config = click.make_pass_decorator(InstanceConfig, ensure=True)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--dir', type=click.Path(), default='./rootserver')
@click.option('--install', is_flag=True)
def setup_root(dir, install):
    os.makedirs(dir, exist_ok=True)
    lgsm_script_path = os.path.join(dir, 'linuxgsm.sh')
    lgsm_script = requests.get(lgsm_dl_url, stream=True)
    with open(lgsm_script_path, 'wb') as f:
        for chunk in lgsm_script.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    st = os.stat(lgsm_script_path)
    os.chmod(lgsm_script_path, st.st_mode | stat.S_IEXEC)
    _run_script(path=lgsm_script_path,
                args=['csgoserver'])
    if install:
        csgoserver_script_path = os.path.join(dir, 'csgoserver.sh')
        _run_script(path=csgoserver_script_path,
                    args=['auto-install'],
                    action_msg="INSTALLING CSGO")

@cli.group()
@click.option('--num-servers', default=8)
@click.option('--start-at', default=1)
@click.option('--server-dir', type=click.Path(), default='./servers')
@pass_instance_config
def instances(config, num_servers, start_at, server_dir):
    config.num_servers = num_servers
    config.start_at = start_at
    config.server_dir = server_dir

@instances.command()
@pass_instance_config
def scaffold(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        os.makedirs(os.path.join(config.server_dir, '{:02}'.format(i)))
        os.makedirs(os.path.join(config.server_dir, '.{:02}'.format(i), 'upper'))
        os.makedirs(os.path.join(config.server_dir, '.{:02}'.format(i), 'work'))

@instances.command()
@click.option('--root-dir', type=click.Path(), default='./rootserver')
@pass_instance_config
def mount(config, root_dir):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="mount_server.sh",
                    args=['{:02}'.format(i), root_dir, config.server_dir],
                    action_msg="Mounting server {:02}".format(i))

@instances.command()
@pass_instance_config
def unmount(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="unmount_server.sh",
                    args=['{:02}'.format(i), config.server_dir],
                    action_msg="Unmounting server {:02}".format(i))

@instances.command()
@pass_instance_config
def remount(config):
    for i in range(config.start_at, config.start_at + config.num_servers):
        _run_script(script="remount_server.sh",
                    args=['{:02}'.format(i), config.server_dir],
                    action_msg="Remounting server {:02}".format(i))

