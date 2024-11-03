#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script manages EC2 instances by having functions for starting and stopping instances with the env: dev tags. 
#It retrieves the instance IDs based on the tag and either starts or stops them.

import boto3

#Comment: This initializes the EC2 client.

ec2 = boto3.client('ec2')

#Comment: This defines and describes the stop instances tagged with the env: dev tag.

def Stop_EC2():
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

#Comment: This defines and describes the start instances tagged with the env: dev tag.

def Start_EC2():
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

#Comment: This calls stop and start functions and prints the responses.

def main():
    print(Stop_EC2())
    print(Start_EC2())

if __name__ == "__main__":
    main()