import click
import boto3
import botocore

# Create an AWS session using your credentials
session = boto3.Session(region_name='us-east-1')  # Replace with your desired AWS region

# Create an EC2 client using the session
ec2_client = session.client('ec2')

@click.group()
@click.option('--debug/--no-debug', default=False, help='Enable or disable debug mode (default: disabled)')
def cli(debug):
    if debug:
        click.echo('Debug mode is enabled')

@cli.command(help='Lists all AWS instances')
def list():
    response = ec2_client.describe_instances()
    reservations = response['Reservations']

    instances_list = []

    for reservation in reservations:
        instances = reservation['Instances']
        for instance in instances:
            instance_id = instance['InstanceId']
            tags = instance.get('Tags', [])
            name_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), None)
            state = instance['State']['Name']
            instances_list.append((instance_id, name_tag, state))

    # Sort the instances based on their state
    instances_list.sort(key=lambda x: (x[2] != 'running', x[2] != 'stopped', x[2] != 'terminated'))

    for instance_id, name_tag, state in instances_list:
        click.echo(f"Instance ID: {instance_id}")
        click.echo(f"Name: {name_tag}")
        click.echo(f"State: {state}")
        click.echo("-" * 30)

@cli.command(help='View info about AWS instance')
@click.option('--instance-id', prompt='Instance ID', help='ID of the instance to gather information about')
def info(instance_id):
    try:
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        reservations = response['Reservations']
        if reservations:
            instances = reservations[0]['Instances']
            if instances:
                instance = instances[0]
                instance_data = {
                    'Cloud': 'aws',
                    'Region': session.region_name,
                    'Id': instance['InstanceId'],
                    'Type': instance['InstanceType'],
                    'ImageId': instance['ImageId'],
                    'State': instance['State']['Name'],
                    'SubnetId': instance.get('SubnetId', None),
                    'VpcId': instance.get('VpcId', None),
                    'MacAddress': None,
                    'NetworkInterfaceId': None,
                    'PrivateDnsName': instance['PrivateDnsName'],
                    'PrivateIpAddress': instance.get('PrivateIpAddress', None),
                    'PublicDnsName': instance.get('PublicDnsName', None),
                    'PublicIpAddress': instance.get('PublicIpAddress', None),
                    'RootDeviceName': instance['RootDeviceName'],
                    'RootDeviceType': instance['RootDeviceType'],
                    'SecurityGroups': instance['SecurityGroups'],
                    'Tags': instance['Tags'] if any(tag['Key'] == 'Name' for tag in instance['Tags']) else [],
                    'LaunchTime': instance['LaunchTime'].strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    'StateReason': None if instance['State']['Name'] == 'running' else instance['StateTransitionReason']
                }
                for key, value in instance_data.items():
                    click.echo(f"{key}: {value}")
            else:
                click.echo(f"No instance found with ID: {instance_id}")
    except botocore.exceptions.ClientError as e:
        click.echo(f"An error occurred: {e}")

@cli.command(help='Stop an AWS instance')
@click.option('--instance-id', prompt='Instance ID', help='ID of the instance to stop')
def stop(instance_id):
    try:
        confirmation = click.confirm(f"Are you sure you wish to stop instance '{instance_id}'?")
        if confirmation:
            response = ec2_client.stop_instances(InstanceIds=[instance_id])
            click.echo(f"Stopping instance: {instance_id}")
            click.echo(f"Performed stop on instance: {instance_id}")
        else:
            click.echo("Operation cancelled.")
    except botocore.exceptions.ClientError as e:
        click.echo(f"An error occurred: {e}")

@cli.command(help='Start an AWS instance')
@click.option('--instance-id', prompt='Instance ID', help='ID of the instance to start')
def start(instance_id):
    try:
        confirmation = click.confirm(f"Are you sure you wish to start instance '{instance_id}'?")
        if confirmation:
            response = ec2_client.start_instances(InstanceIds=[instance_id])
            click.echo(f"Starting instance: {instance_id}")
            click.echo(f"Performed start on instance: {instance_id}")
        else:
            click.echo("Operation cancelled.")
    except botocore.exceptions.ClientError as e:
        click.echo(f"An error occurred: {e}")

@cli.command(help='Terminate an AWS instance')
@click.option('--instance-id', prompt='Instance ID', help='ID of the instance to terminate')
def terminate(instance_id):
    try:
        confirmation = click.confirm(f"Are you sure you wish to terminate instance '{instance_id}'?")
        if confirmation:
            response = ec2_client.terminate_instances(InstanceIds=[instance_id])
            click.echo(f"Terminating instance: {instance_id}")
            click.echo(f"Performed terminate on instance: {instance_id}")
        else:
            click.echo("Operation cancelled.")
    except botocore.exceptions.ClientError as e:
        click.echo(f"An error occurred: {e}")


if __name__ == '__main__':
    cli()

