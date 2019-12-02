#To get stopped or running instances we can use filters --> these are collections
import boto3
session=boto3.session.Session(profile_name="default")
instances_list=session.resource(service_name="ec2",region_name="us-east-1")
f1={"Name": "instance-state-name" ,"Values":['stopped','running']}
for instancestatus in instances_list.instances.filter(Filters=[f1]):
  print(instancestatus.id,instancestatus.state)