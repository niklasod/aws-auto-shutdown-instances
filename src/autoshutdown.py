import boto3
from datetime import datetime, timezone, timedelta
from os import environ
import logging
logger = logging.getLogger("aws-autoshutdown")
logger.setLevel("INFO")

ec2 = boto3.client("ec2")

ec2session = boto3.Session()
ec2resource = ec2session.resource("ec2")



def tag_list(tags_param):
    return tags_param.split(",")

def stop_instances(instances):
    logger.info(f"Stopping the found instances with ids: {instances}")
    ec2.stop_instances(InstanceIds=instances)

def get_parameters():
    logger.info("Fetching parameters from the parameters store")
    ssm = boto3.client("ssm")
    params_response = ssm.get_parameters(
        Names=[
            '/syso/auto-shutdown/max-age',
            '/syso/auto-shutdown/tags'
        ]
    )
    for parameter in params_response["Parameters"]:
        if parameter["Name"] == '/syso/auto-shutdown/max-age':
            max_age = parameter["Value"]
        if parameter["Name"] == '/syso/auto-shutdown/tags':
            tags_param = parameter["Value"]

    return max_age, tags_param

def handler(event, context):
    logger.info("Fetching all running instances to check for tagging and potential shutdown")
    instances = ec2resource.instances.filter(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            }
        ]
    )
    max_age, tags_param = get_parameters()
    tags = tag_list(tags_param)
    stop_instances_list = []
    if len(list(instances)) == 0:
       logger.info("Found no instances running. Exiting.")
    else:
        logger.info(f"{len(list(instances))} found running. Checking if they are tagged with any of these tag keys: {tags} and have been running for more than {max_age} days")
        for instance in instances:
            instance_tags = instance.tags
            if instance_tags is None or not any(t["Key"] in tags for t in instance_tags) and datetime.now(timezone.utc) - instance.launch_time > timedelta(days=int(max_age)):
                logger.info(f"Instance with id {instance.id} does not have the 'keep running' tags ({tags}) with age older than {max_age} days. It will be stopped")
                stop_instances_list.append(instance.id)
            else:
                logger.info(f"Instance with id {instance.id} was tagged with 'keep running' tags or has been running for less than {max_age} days. Will keep running")
    if len(stop_instances_list) > 0:
        stop_instances(stop_instances_list)
  