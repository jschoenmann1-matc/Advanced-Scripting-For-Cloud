#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This Lambda function is triggered to start EC2 instances with the env: dev tag.
#This retrieves instance IDs based on the tag and starts them, then logs the instance IDs that were started.


import json
import boto3

#Comment: This defines and describes the start instances tagged with the env: dev tag.

def Start_EC2():
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:env',
                'Values': ['dev']
            }
        ]
    )
    instance_list = []
    for reservation in response['Reservations']:
        for instance in reservation ['Instances']:
            #print(instance['InstanceId'])
            instance_list.append(instance['InstanceId'])

#Comment: This starts the instances based on the collected IDs.

    start_response = ec2.start_instances(InstanceIds=instance_list)
    return start_response

#Comment: This handler invokes the Start_EC2 function to log started instances.

def lambda_handler(event, context):
    # TODO implement
    response = Start_EC2()
    for instance in response['StartingInstances']:
        print(instance['InstanceId'])

#Comment: This gives a return response for Lambda invocation.

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
