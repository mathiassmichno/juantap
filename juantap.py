import os
import stat
import subprocess
import shutil
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
    cfg['system'] = {
        'JuantapUser' : getpass.getuser(),
        'RootServerDir' : os.path.expanduser('~/rootserver'),
        'InstancesDir' : os.path.expanduser('~/instances'),
        'NumberOfInstances' : 2,
        'BaseHostname': "Juantap",
    }
    write_config()

cfg.read(CONFIG_PATH)
script_folder=os.path.join(os.path.dirname(__file__), "scripts")
lgsm_dl_url="https://raw.githubusercontent.com/mathiassmichno/LinuxGSM/master/linuxgsm.sh"

def _run_script(script="", path=None, args=(), action_msg=""):
    if not path:
        path = os.path.join(script_folder, script)
    try:
        subprocess.run([path, *args], stderr=subprocess.STDOUT, check=True)
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

@cli.group()
@click.option('--dir', 'root_dir', type=click.Path(), default=cfg['system']['RootServerDir'], help="Path to root server directory")
@click.pass_context
def root(ctx, root_dir):
    """
    Control server instances from here
    """
    if root_dir != cfg['system']['RootServerDir']:
        cfg['system']['RootServerDir'] = root_dir

@root.command()
@click.option('--install', is_flag=True)
@click.confirmation_option(help='Are you sure you want to set up a rootserver?')
@click.pass_context
def setup(ctx, install):
    """
    Setup root server, see --help for more
    """
    root_dir = cfg['system']['RootServerDir']
    click.confirm('Set up root server in "{}"?'.format(root_dir), abort=True)
    os.makedirs(root_dir, exist_ok=True)
    os.chdir(root_dir)
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
        csgoserver_script_fname = 'csgoserver'
        _run_script(path=csgoserver_script_fname,
                    args=['auto-install'])

@cli.group()
@click.option('--instances-dir', type=click.Path(), default=cfg['system']['InstancesDir'])
@click.option('--num-instances', type=int, default=int(cfg['system']['NumberOfInstances']))
@click.option('--instance', '-i', multiple=True)
@click.pass_context
def instances(ctx, instances_dir, num_instances, instance):
    """
    Control server instances from here
    """
    if instances_dir != cfg['system']['InstancesDir']:
        cfg['system']['InstancesDir'] = instances_dir
    ctx.obj = {'instances': instance if instance else ['{:02}'.format(i) for i in range(1, int(num_instances) + 1)]}


@instances.command()
@click.argument('command')
@click.pass_context
def cmd(ctx, command):
    for instance in ctx.obj['instances']:
        click.echo('Sending {} command to instance {}'.format(command, instance))
        _run_script(path=os.path.join(cfg['system']['InstancesDir'], instance, instance),
                    args=[command,])

@instances.command()
@click.pass_context
def scaffold(ctx):
    """
    Scaffold the folders for instances
    """
    for instance in ctx.obj['instances']:
        click.echo('Scaffolding instance {}'.format(instance))
        os.makedirs(os.path.join(cfg['system']['InstancesDir'], instance))
        os.makedirs(os.path.join(cfg['system']['InstancesDir'], instance, 'upper'))
        os.makedirs(os.path.join(cfg['system']['InstancesDir'], instance, 'work'))


@instances.command()
@click.pass_context
def setup(ctx):
    """
    Setup instances
    """
    for instance in ctx.obj['instances']:
        inst_dir = os.path.join(cfg['system']['InstancesDir'], instance)
        csgoscript_path = os.path.join(inst_dir, 'csgoserver')
        instscript_path = os.path.join(inst_dir, '{}'.format(instance))
        shutil.copy2(csgoscript_path, instscript_path)
        inst_default_cfg = {
            'port': 27015 + int(instance) * 100,
            'clientport': 27005 + int(instance) * 100,
            'sourcetvport': 27020 + int(instance) * 100,
            'gslt': '"$(sed -n \'{}p\' ~/gslts.txt)"'.format(int(instance)),
            'hostname': '"{} - {}"'.format(cfg['system']['BaseHostname'], instance),
            'rcon_password': '"{}"'.format(id(instance)),
        }
        existing_cfg = cfg[instance] if instance in cfg.sections() else {}
        cfg[instance] = {**inst_default_cfg, **existing_cfg}
        instconfig_path = os.path.join(inst_dir, 'lgsm/config-lgsm/csgoserver/{}.cfg'.format(instance))
        with open(instconfig_path, 'w') as file:
            print('# AUTO-GENERATED BY JUANTAP\n# DO NOT EDIT THIS FILE\n# IT WILL BE OVERWRITTEN!', file=file)
            for k, v in cfg[instance].items():
                print('{}={}'.format(k, v), file=file)
    write_config()


@instances.command()
@click.option('--root-dir', type=click.Path(), default=cfg['system']['RootServerDir'])
@click.pass_context
def mount(ctx, root_dir):
    """
    Mount instances to root server with overlayfs
    """
    for instance in ctx.obj['instances']:
        click.echo('Mounting instance {}'.format(instance))
        _run_script(script="mount_server.sh",
                    args=[instance, root_dir, cfg['system']['InstancesDir']])


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
                    args=[instance, cfg['system']['InstancesDir']])


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
                    args=[instance, cfg['system']['InstancesDir']])


@instances.command()
@click.pass_context
def remove(ctx):
    click.confirm('Remove instances: {}? (Cannot be reverted)'.format(ctx.obj['instances']), abort=True)
    ctx.invoke(unmount)
    for instance in ctx.obj['instances']:
        click.echo('Removing instance {}'.format(instance))
        shutil.rmtree(os.path.join(cfg['system']['InstancesDir'], instance))
        try:
            del cfg[instance]
        except:
            pass #  Maybe the user deleted config section
    write_config()
