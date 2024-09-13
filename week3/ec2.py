#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script launches an Amazon EC2 instance, adds a name tag to it, and terminates the instance when done.
#This uses Boto3 to manage the instance and applies some basic filtering to find the Amazon AMI.

import boto3
import json

#Comment: This gets the latest Amazon AMI image based on the filters provided below.

def Get_Image(ec2client):
    image_response = ec2client.describe_images(
        Filters=[
            {
                'Name': 'description',
                'Values': ['Amazon Linux 2 AMI*']
            },
            {
                'Name': 'architecture',
                'Values': ['x86_64']
            },
            {
                'Name': 'owner-alias',
                'Values': ['amazon']
            }
        ]
    )
    return image_response['Images'][0]['ImageId']

#Comment: This function creates an EC2 instance using the AMI provided.

def Create_EC2(AMI, ec2client):

    DRYRUN = False


    response = ec2client.run_instances(
        ImageId=AMI,
        InstanceType='t2.micro',
        MaxCount=1,
        MinCount=1,
        DryRun=DRYRUN
    )
    return response['Instances'][0]['InstanceId']

#Comment: This is the main function of the script to get the latest Amazon image, launch an EC2 instance and get the ID and manage the lifecycle.

def main():
    client = boto3.client('ec2')
    AMI = Get_Image(client)

    instance_id = Create_EC2(AMI, client)

    ec2 = boto3.resource('ec2')
    instance = ec2.Instance(instance_id)


#Comment: This prints an instance state before waiting, then waits for the instance to be fully running. 

    print(f"Before Waiting: Instance is {instance.state['Name']}")
    instance.wait_until_running()
    instance.load()
    print(f"After Waiting: Instance is {instance.state['Name']}")
    print(f"Public IP Address: {instance.public_ip_address}")

#Comment: This checks for any existing tags on the instance, prints them, and adds a Name tag if there are none.

    if instance.tags:
        print(f"Tags before adding: {instance.tags}")
    else:
        print("No tags found before adding")

    instance.create_tags(
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Jordan'
            }
        ]
    )

#Comment: This reloads the instance data to show the new tag and terminates once done and waits until it's fully finished.

    instance.load()
    print(f"Updated Tags: {instance.tags}")

    print(f"Before Termination: Instance is {instance.state['Name']}")
    instance.terminate()
    instance.wait_until_terminated()
    print(f"After Terminated: Instance is {instance.state['Name']}")

if __name__ == "__main__":
    main()