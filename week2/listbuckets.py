#!/usr/bin/env python3
#Author: Jordan Sexton-Schoenmann

#General Description: This script will connect to AWS using the boto3 library, list all 
#of the S3 buckets in the account, and print out the name of each bucket.


#Comment: This imports boto3 to interact with AWS and s3client enables API calls.
import boto3

s3client = boto3.client('s3')


#Comment: This calls for the list_buckets method and returns a dictionary containing all of the s3 buckets in my AWS account.
bucket_list = s3client.list_buckets()


#Comment: This goes over each bucket in the bucket_list and prints the name of each. Then list_objects_v2 lists all of the files in the current bucket.
#Then if 'Contents' checks if there are any objects in the response and if there is, loops through them and prints the object names or doesn't and outputs a response.
for bucket in bucket_list['Buckets']:
    print(f"Bucket Name is: {bucket['Name']}")

    response = s3client.list_objects_v2(Bucket=bucket['Name'])

    if 'Contents' in response:
        for obj in response['Contents']:
            print(f" Object Name: {obj['Key']}")

    else:
        print("No objects in this bucket.")