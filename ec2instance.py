import boto3


class aws:
    
    ec2 = boto3.resource('ec2')
    ec1 = boto3.client('ec2')

    try:
        response = ec1.describe_security_groups()
        secgroup=response['SecurityGroups'][0]['GroupName']
        secgroupid=response['SecurityGroups'][0]['GroupId']
                         
        if  secgroup == 'ALL-PYTHON':
            print("security group already exists")
            instances = ec2.create_instances(
            ImageId='ami-07d0cf3af28718ef8',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='python-boto',
            NetworkInterfaces=[{
            'DeviceIndex': 0,
            'SubnetId': 'subnet-12210275',
            'Groups': [secgroupid]
            }],
            )    
       
        else:
            securitygroup = ec2.create_security_group(GroupName='ALL-PYTHON',Description='Allow ALL Traffic')
            securitygroup.authorize_ingress(
            CidrIp='0.0.0.0/0',
            IpProtocol='-1',
            FromPort=0,
            ToPort=0
            )
            instances = ec2.create_instances(
            ImageId='ami-07d0cf3af28718ef8',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='python-boto',
            NetworkInterfaces=[{
            'DeviceIndex': 0,
            'SubnetId': 'subnet-12210275',
            'Groups': [securitygroup.group_id]
            }],
            )    
        
    except Exception as e:
        print(e)
