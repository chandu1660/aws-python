#waiters can be used to block until certain state has been reached
#Below code used to stop the instance it will not exit from the prompt until instance stops
#waiters default time period is 200 seconds for every 5 seconds it will check
import boto3
session=boto3.session.Session(profile_name="default")
instances_list=session.resource(service_name="ec2",region_name="us-east-1")
Instance_status=instances_list.Instance(id="i-00e1898cfcf905c41")
Instance_status.stop()
Instance_status.wait_until_stopped()