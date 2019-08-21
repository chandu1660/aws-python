import base64
import json
import os
import subprocess
import boto3
import docker

ECS_CLUSTER = 'practice-cluster'
ECS_SERVICE = 'practice-service'

LOCAL_REPOSITORY = 'practice-python'
client = boto3.client('ecr')

def main():
    """Build Docker image, push to AWS and update ECS service.

    :rtype: None
    """

    # get AWS credentials
    aws_credentials = read_aws_credentials()
    access_key_id = aws_credentials['access_key_id']
    secret_access_key = aws_credentials['secret_access_key']
    aws_region = aws_credentials['region']
    print(access_key_id)
    print(secret_access_key)
    print(aws_region)

    # build Docker image
    docker_client = docker.from_env()
    image, build_log = docker_client.images.build(
        path='.', tag=LOCAL_REPOSITORY, rm=True)

    # get AWS ECR login token
    ecr_client = boto3.client(
        'ecr', aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key, region_name=aws_region)
    ecr_credentials = (
        ecr_client
        .get_authorization_token()
        ['authorizationData'][0])
    ecr_username = 'AWS'
    ecr_password = (
        base64.b64decode(ecr_credentials['authorizationToken'])
        .replace(b'AWS:', b'')
        .decode('utf-8'))
    ecr_url = ecr_credentials['proxyEndpoint']
    # get Docker to login/authenticate with ECR
    docker_client.login(
        username=ecr_username, password=ecr_password, registry=ecr_url, reauth=True)
    # tag image for AWS ECR
    ecr_repo_name = '{}/{}'.format(
        ecr_url.replace('https://',''), LOCAL_REPOSITORY)
    image.tag(ecr_repo_name, tag='latest')

    # push image to AWS ECR
    push_log = docker_client.images.push(ecr_repo_name, tag='latest')
    print(push_log)
    # force new deployment of ECS service
    ecs_client = boto3.client(
        'ecs', aws_access_key_id=access_key_id,
        aws_secret_access_key=secret_access_key, region_name=aws_region)

    ecs_client.update_service(
        cluster=ECS_CLUSTER, service=ECS_SERVICE, forceNewDeployment=True)
    return None

    
def read_aws_credentials(filename='.aws_credentials.json'):
    """Read AWS credentials from file.

    :param filename: Credentials filename, defaults to '.aws_credentials.json'
    :param filename: str, optional
    :return: Dictionary of AWS credentials.
    :rtype: Dict[str, str]
    """

    try:
        with open(filename) as json_data:
            credentials = json.load(json_data)

        for variable in ('access_key_id', 'secret_access_key', 'region'):
            if variable not in credentials.keys():
                msg = '"{}" cannot be found in {}'.format(variable, filename)
                raise KeyError(msg)

    except FileNotFoundError:
        try:
            credentials = {
                'access_key_id': os.environ['AWS_ACCESS_KEY_ID'],
                'secret_access_key': os.environ['AWS_SECRET_ACCESS_KEY'],
                'region': os.environ['AWS_REGION']
            }
        except KeyError:
            msg = 'no AWS credentials found in file or environment variables'
            raise RuntimeError(msg)

    return credentials


if __name__ == '__main__':
    main()
