import boto3
import click

session = boto3.Session(profile_name = 'ferrari-lagauzere')
ec2 = session.resource('ec2')

def get_ec2_instances(project):

    ec2_instances = []

    if project:
        print('Looking up instances for ' + project + ' project')
        filters = [{'Name':'tag:Project','Values':['ferrari-lagauzere']}]
        ec2_instances = ec2.instances.filter(Filters=filters)
    else:
        print('project is not set')
        ec2_instances = ec2.instances.all()

    return ec2_instances

@click.group()
def cli():
    "Command Line Intercace"

@cli.group('snapshots')
def snapshots():
    "Snapshots Commands"

@snapshots.command('list')
@click.option('--project', default=None, help="Instances project")
def list_snapshots(project):
    "List EC2 insteance volume snapshots"
    
    for i in get_ec2_instances(project):
        for v in i.volumes.all():
            for s in v.snapshots.all():
                click.echo('Snapshots >> ' + ', '.join([i.id, v.volume_id, s.snapshot_id, s.description, s.state, s.start_time.strftime("%c"), s.progress]))
    return

@cli.group('volumes')
def volumes():
    "Volumes Commands"

@volumes.command('list')
@click.option('--project', default=None, help="Instances project")
def list_volumes(project):
    "List EC2 insteance volumes"
    
    for i in get_ec2_instances(project):
        for v in i.volumes.all():
            click.echo('Volumes >> ' + ', '.join([i.id, v.volume_id, v.availability_zone, v.encrypted and "Encrypted" or "Not encrypted", str(v.size) + "GiB", v.volume_type, v.state]))
    return


@cli.group('instances')
def instances():
    "Instances Commands"

@instances.command('list')
@click.option('--project', default=None, help="Instances project")
def list_instances(project):

    "List EC2 instances"
    
    for i in get_ec2_instances(project):
       click.echo('Instance >> ' + ', '.join([i.id, i.hypervisor, i.placement['AvailabilityZone'], i.instance_type, i.platform, i.state['Name']]))
    return

@instances.command('stop')
@click.option('--project', default=None, help="Instances project")
def stop_instances(project):

    "Stop EC2 instances"
    
    for i in get_ec2_instances(project):
        click.echo('Stopping instance ' + str(i))
        i.stop()
    return

@instances.command('start')
@click.option('--project', default=None, help="Instances project")
def start_instances(project):

    "Start EC2 instances"
        
    for i in get_ec2_instances(project):
        click.echo('Starting instance ' + str(i))
        i.start()
    return

# Remember the entry point when the execusion is done as a script
if __name__ == '__main__':
    cli()