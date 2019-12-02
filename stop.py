import boto3
session=boto3.session.Session(profile_name="default")
instances_list=session.resource(service_name="ec2",region_name="us-east-1")

Instance_status=instances_list.Instance(id="i-00e1898cfcf905c41")
Instance_status.stop()