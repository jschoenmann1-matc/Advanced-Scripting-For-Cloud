#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This Lambda function is triggered to stop EC2 instances with the env: dev tag.
#This retrieves instance IDs based on the tag and stops them, then logs the instance IDs that were stopped.

import json
import boto3

#Comment: This defines and describes the stop instances tagged with the env: dev tag.

def Stop_EC2():
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

#Comment: This stops the instances based on the collected IDs.

    stop_response = ec2.stop_instances(InstanceIds=instance_list)
    return stop_response

#Comment: This handler invokes the Stop_EC2 function to log stopped instances.

def lambda_handler(event, context):
    # TODO implement
    response = Stop_EC2()
    for instance in response['StoppingInstances']:
        print(instance['InstanceId'])

#Comment: This gives a return response for Lambda invocation.

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
