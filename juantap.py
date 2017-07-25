import os
import stat
import subprocess
import click
import requests
import time
from configparser import ConfigParser
import getpass

APP_DIR = click.get_app_dir('juantap')
CONFIG_PATH = os.path.join(APP_DIR, 'config.ini')

cfg = ConfigParser()

def write_config():
    global cfg
    with open(CONFIG_PATH, 'w') as cfg_file:
        cfg.write(cfg_file)


if not os.path.exists(CONFIG_PATH):
    os.makedirs(APP_DIR, exist_ok=True)
    cfg['DEFAULT'] = {
        'JuantapUser' : getpass.getuser(),
        'RootServerDir' : os.path.expanduser('~/rootserver'),
        'InstancesDir' : os.path.expanduser('~/instances'),
        'NumberOfInstances' : 2,
    }
    write_config()

cfg.read(CONFIG_PATH)
script_folder=os.path.join(os.path.dirname(__file__), "scripts")
lgsm_dl_url="https://gameservermanagers.com/dl/linuxgsm.sh"

def _run_script(script="", path=None, args=(), action_msg=""):
    if not path:
        path = os.path.join(script_folder, script)
    try:
        subprocess.run([path, *args], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)
    except subprocess.CalledProcessError as e:
        click.ClickException(e)

@click.group()
def cli():
    """
    CLI for managing multiple csgo server instances and their root server.

    Harnesses the power of overlayfs
    """
    pass

@cli.group(invoke_without_command=True, chain=True)
@click.option('-e', is_flag=True, help='open config in editor')
@click.pass_context
def config(ctx, e):
    if e:
        click.edit(filename=os.path.join(APP_DIR, 'config.ini'))
    else:
        click.echo(ctx.get_help())


@cli.command()
@click.option('--dir', type=click.Path(), default=cfg['DEFAULT']['RootServerDir'])
@click.option('--install', is_flag=True)
@click.confirmation_option(help='Are you sure you want to set up a rootserver?')
def setup(dir, install):
    """
    Setup root server, see --help for more
    """
    click.confirm('Set up root server in "{}"?'.format(dir), abort=True)
    os.makedirs(dir, exist_ok=True)
    os.chdir(dir)
    lgsm_script_fname = 'linuxgsm.sh'
    click.echo('Downloading Linux Game Server Manager Script')
    lgsm_script = requests.get(lgsm_dl_url, stream=True)
    with open(lgsm_script_fname, 'wb') as f:
        for chunk in lgsm_script.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    st = os.stat(lgsm_script_fname)
    os.chmod(lgsm_script_fname, st.st_mode | stat.S_IEXEC)
    _run_script(path=lgsm_script_fname,
                args=['csgoserver'])
    if install:
        click.echo('Installing CS:GO in root server')
        csgoserver_script_fname = 'csgoserver.sh'
        _run_script(path=csgoserver_script_fname,
                    args=['auto-install'])

@cli.group()
@click.option('--instances-dir', type=click.Path(), default=cfg['DEFAULT']['InstancesDir'])
@click.option('--num-instances', type=int, default=int(cfg['DEFAULT']['NumberOfInstances']))
@click.option('--instance', '-i', multiple=True)
@click.pass_context
def instances(ctx, instances_dir, num_instances, instance):
    """
    Control server instances from here
    """
    if instances_dir != cfg['DEFAULT']['InstancesDir']:
        cfg['DEFAULT']['InstancesDir'] = instances_dir
    ctx.obj = {'instances': instance if instance else ['{:02}'.format(i) for i in range(1, int(num_instances) + 1)]}

@instances.command()
@click.pass_context
def scaffold(ctx):
    """
    Scaffold the folders for instances, and config file entries
    """
    for instance in ctx.obj['instances']:
        click.echo('Scaffolding instance {}'.format(instance))
        os.makedirs(os.path.join(cfg['DEFAULT']['InstancesDir'], instance))
        os.makedirs(os.path.join(cfg['DEFAULT']['InstancesDir'], instance, 'upper'))
        os.makedirs(os.path.join(cfg['DEFAULT']['InstancesDir'], instance, 'work'))
        cfg[instance] = {
            'basePort': 27014 + int(instance),
            'glst': '',
            'Hostname': str(instance),
        }
    write_config()

@instances.command()
@click.option('--root-dir', type=click.Path(), default=cfg['DEFAULT']['RootServerDir'])
@click.pass_context
def mount(ctx, root_dir):
    """
    Mount instances to root server with overlayfs
    """
    for instance in ctx.obj['instances']:
        click.echo('Mounting instance {}'.format(instance))
        _run_script(script="mount_server.sh",
                    args=[instance, root_dir, cfg['DEFAULT']['InstancesDir']])

@instances.command()
@click.confirmation_option(help='Are you sure you want to unmount?')
@click.pass_context
def unmount(ctx):
    """
    Unmount instances
    """
    for instance in ctx.obj['instances']:
        click.echo('Unmounting instance {}'.format(instance))
        _run_script(script="unmount_server.sh",
                    args=[instance, cfg['DEFAULT']['InstancesDir']])

@instances.command()
@click.confirmation_option(help='Are you sure you want to remount?')
@click.pass_context
def remount(ctx):
    """
    Remount instances, updates root server changes
    """
    for instance in ctx.obj['instances']:
        click.echo('Remounting instance {}'.format(instance))
        _run_script(script="remount_server.sh",
                    args=[instance, cfg['DEFAULT']['InstancesDir']])

