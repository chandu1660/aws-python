import boto3
ec2=boto3.client('ec2')
session=boto3.session.Session(profile_name="default")
instances_list=session.resource(service_name="ec2",region_name="us-east-1")
sggroups=ec2.describe_security_groups()
x=session.get_available_resources()
print(x)

print(sggroups)
for instances_id in instances_list.instances.all():
    print(instances_id.id,instances_id.state) 