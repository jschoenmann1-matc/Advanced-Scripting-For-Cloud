#Author: Jordan Sexton-Schoenmann

#General Description: This script is an AWS Lambda function that stops all running EC2 instances. It identifies any EC2 instances in a running state
#and stops them. If nothing is found, it will return a message indicating nothing to stop. 

import boto3
import json

#Comment: This part defines the region and creates and EC2 client to interact with the AWS EC2 service.

region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)

#Comment: Describes instances with the running state and only the running instances.

def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
            ]
        },
    ],
    )

#Comment: This initializes a list of ID's to be started and loops through the reservations and also prints and appends each instance ID that is currently running.

    listofinstanceids = []
    for reservation in response["Reservations"]:
        instances = reservation["Instances"]
    
        for instance in instances:
             print(instance["InstanceId"])
             listofinstanceids.append(instance["InstanceId"])
    
#Comment: This stops any instances if any are running and prints the message for logging.

    stop_response = "Nothing needed to be stopped"
    if len(listofinstanceids) != 0:
        stop_response = ec2.stop_instances(InstanceIds=listofinstanceids,DryRun=False)
    print(stop_response)
    return {
        'statusCode': 200,
        'body': json.dumps(stop_response)
    }