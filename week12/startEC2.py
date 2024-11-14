#Author: Jordan Sexton-Schoenmann

#General Description: This script is an AWS Lambda function that starts all stopped EC2 instances. It identifies any EC2 instances in a stopped state
#and starts them. If nothing is found, it will return a message indicating nothing to start. 

import boto3
import json

#Comment: This part defines the region and creates and EC2 client to interact with the AWS EC2 service.

region = 'us-east-1'
ec2 = boto3.client('ec2', region_name=region)

#Comment: Describes instances with the stopped states and only the stopped instances.

def lambda_handler(event, context):
    response = ec2.describe_instances(
        Filters=[
        {
            'Name': 'instance-state-name',
            'Values': [
                'stopped',
            ]
        },
    ],
    )

#Comment: This initializes a list of ID's to be started and loops through the reservations and also prints and appends each instance ID that is currently stopped.

    list_of_instance_ids = []
    for reservation in response["Reservations"]:
        instances = reservation["Instances"]
    
        for instance in instances:
             print(instance["InstanceId"])
             list_of_instance_ids.append(instance["InstanceId"])

#Comment: This starts any instances if any are stopped and prints the message for logging.

    if list_of_instance_ids:
        start_response = ec2.start_instances(InstanceIds=list_of_instance_ids)
        print(start_response)
        return {
            'statusCode': 200,
            'body': json.dumps(start_response)
        }

#Comment: This is the return message if no instances need to be started.

    else:
        return {
            'statusCode': 200,
            'body': json.dumps("No instances to start.")
        }
