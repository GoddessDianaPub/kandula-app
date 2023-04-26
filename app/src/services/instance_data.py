from boto3 import client

REGION_NAME = 'us-east-1'

def get_state_reason(instance):
    instance_state = instance['State']['Name']
    if instance_state != 'running':
        return instance['StateReason']['Message']

class InstanceData:

    def __init__(self, ec2_client: client):
        self.ec2_client = ec2_client

    def get_instances(self):
        instances_data = []
        response = self.ec2_client.describe_instances()
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_data = {
                    'Cloud': 'aws',
                    'Region': REGION_NAME,
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
         #           'Tags': instance['Tags'],
                    'Tags': instance['Tags'] if any(tag['Key'] == 'Name' for tag in instance['Tags']) else [],
                    'LaunchTime': instance['LaunchTime'].strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    'StateReason': None if instance['State']['Name'] == 'running' else instance['StateTransitionReason'],
                }
                if instance['NetworkInterfaces']:
                    instance_data['MacAddress'] = instance['NetworkInterfaces'][0]['MacAddress']
                    instance_data['NetworkInterfaceId'] = instance['NetworkInterfaces'][0]['NetworkInterfaceId']

                instances_data.append(instance_data)
                
        # Sort the instances by the value of the "Name" tag
        instances_data = sorted(instances_data, key=lambda i: (-1 if i['State'] == 'running' else 1, [t['Value'] for t in i['Tags'] if t['Key'] == 'Name']))
      #  instances_data = sorted(instances_data, key=lambda i: [t['Value'] for t in i['Tags'] if t['Key'] == 'Name'])
        
        return {'Instances': instances_data}
    
