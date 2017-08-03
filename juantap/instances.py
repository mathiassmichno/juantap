import os
import shutil
import getpass
from functools import partial
import click
import sh

from . import CFG, write_config

@click.group()
@click.option('--instances-dir', type=click.Path(), default=CFG['system']['InstancesDir'])
@click.option('--num-instances', type=int, default=int(CFG['system']['NumberOfInstances']))
@click.option('--instance', '-i', multiple=True)
@click.pass_context
def instances(ctx, instances_dir, num_instances, instance):
    """
    Control server instances from here
    """
    if instances_dir != CFG['system']['InstancesDir']:
        CFG['system']['InstancesDir'] = instances_dir
    ctx.obj = {'instances': instance if instance else ['{:02}'.format(i) for i in range(1, int(num_instances) + 1)]}


@instances.command()
@click.option('-p', is_flag=True, help="Use pager to display command output")
@click.argument('command')
@click.pass_context
def cmd(ctx, p, command):
    for instance in ctx.obj['instances']:
        click.echo('Sending "{}" command to instance {}'.format(command, instance))
        inst_script = sh.Command(os.path.join(CFG['system']['InstancesDir'], instance, instance))
        if p:
            click.echo_via_pager(inst_script(command))
        else:
            inst_script(command, _out=partial(click.echo, nl=False))



@instances.command()
@click.pass_context
def scaffold(ctx):
    """
    Scaffold the folders for instances
    """
    for instance in ctx.obj['instances']:
        click.echo('Scaffolding instance {}'.format(instance))
        os.makedirs(os.path.join(CFG['system']['InstancesDir'], instance))
        os.makedirs(os.path.join(CFG['system']['InstancesDir'], '.' + instance, 'upper'))
        os.makedirs(os.path.join(CFG['system']['InstancesDir'], '.' + instance, 'work'))


@instances.command()
@click.pass_context
def setup(ctx):
    """
    Setup instances
    """
    for instance in ctx.obj['instances']:
        inst_dir = os.path.join(CFG['system']['InstancesDir'], instance)
        csgoscript_path = os.path.join(inst_dir, 'csgoserver')
        instscript_path = os.path.join(inst_dir, '{}'.format(instance))
        shutil.copy2(csgoscript_path, instscript_path)
        inst_default_cfg = {
            'port': 27015 + int(instance) * 100,
            'clientport': 27005 + int(instance) * 100,
            'sourcetvport': 27020 + int(instance) * 100,
            'gslt': '"$(sed -n \'{}p\' ~/gslts.txt)"'.format(int(instance)),
            'hostname': '"{} - {}"'.format(CFG['system']['BaseHostname'], instance),
            'rcon_password': '"{}"'.format(id(instance)),
        }
        existing_cfg = CFG[instance] if instance in CFG.sections() else {}
        CFG[instance] = {**inst_default_cfg, **existing_cfg}
        instconfig_path = os.path.join(inst_dir, 'lgsm/config-lgsm/csgoserver/{}.cfg'.format(instance))
        with open(instconfig_path, 'w') as file:
            print('# AUTO-GENERATED BY JUANTAP\n# DO NOT EDIT THIS FILE\n# IT WILL BE OVERWRITTEN!', file=file)
            for k, v in CFG[instance].items():
                print('{}={}'.format(k, v), file=file)
    write_config()


@instances.command()
@click.option('--root-dir', type=click.Path(), default=CFG['system']['RootServerDir'])
@click.pass_context
def mount(ctx, root_dir):
    """
    Mount instances to root server with overlayfs
    """
    click.echo('Sudo needed to mount instances')
    password = getpass.getpass()
    for instance in ctx.obj['instances']:
        click.echo('Mounting instance {}'.format(instance))
        inst_path = os.path.join(CFG['system']['InstancesDir'], instance)
        inst_dot_path = os.path.join(CFG['system']['InstancesDir'], '.' + instance)
        with sh.contrib.sudo(password=password, _with=True):
            sh.mount("-t", "overlay", "-o",
                     "lowerdir={0},upperdir={1}/upper,workdir={1}/work".format(root_dir, inst_dot_path),
                     "overlay", inst_path)


@instances.command()
@click.pass_context
def unmount(ctx):
    """
    Unmount instances
    """
    click.echo('Sudo needed to unmount instances')
    password = getpass.getpass()
    for instance in ctx.obj['instances']:
        click.echo('Unmounting instance {}'.format(instance))
        inst_path = os.path.join(CFG['system']['InstancesDir'], instance)
        with sh.contrib.sudo(password=password, _with=True):
            sh.umount(inst_path, _ok_code=[0,32])


@instances.command()
@click.pass_context
def remount(ctx):
    """
    Remount instances, updates root server changes
    """
    click.echo('Sudo needed to remount instances')
    password = getpass.getpass()
    for instance in ctx.obj['instances']:
        click.echo('Remounting instance {}'.format(instance))
        inst_path = os.path.join(CFG['system']['InstancesDir'], instance)
        with sh.contrib.sudo(password=password, _with=True):
            sh.mount("-o" "remount", inst_path)
        


@instances.command()
@click.pass_context
def remove(ctx):
    click.confirm('Remove instances: {}? (Cannot be reverted)'.format(ctx.obj['instances']), abort=True)
    ctx.invoke(unmount)
    for instance in ctx.obj['instances']:
        click.echo('Removing instance {}'.format(instance))
        shutil.rmtree(os.path.join(CFG['system']['InstancesDir'], instance))
        shutil.rmtree(os.path.join(CFG['system']['InstancesDir'], '.' + instance))
        try:
            del CFG[instance]
        except:
            pass #  Maybe the user deleted config section
    write_config()
