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

CFG = ConfigParser()

def write_config():
    with open(CONFIG_PATH, 'w') as cfg_file:
        CFG.write(cfg_file)


if not os.path.exists(CONFIG_PATH):
    os.makedirs(APP_DIR, exist_ok=True)
    CFG['system'] = {
        'JuantapUser' : getpass.getuser(),
        'RootServerDir' : os.path.expanduser('~/rootserver'),
        'InstancesDir' : os.path.expanduser('~/instances'),
        'NumberOfInstances' : 2,
        'BaseHostname': "Juantap",
    }
    write_config()

CFG.read(CONFIG_PATH)

@click.group()
def cli():
    """
    CLI for managing multiple csgo server instances and their root server.

    Harnesses the power of overlayfs
    """
    pass

from . import config, instances, root

cli.add_command(config.config)
cli.add_command(instances.instances)
cli.add_command(root.root)