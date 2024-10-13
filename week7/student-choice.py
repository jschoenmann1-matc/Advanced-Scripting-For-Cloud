#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script lists all s3 buckets in the AWS account and checks if any buckets have
#any public access and will report on them if they do.

import boto3
from botocore.exceptions import ClientError

#Comment: This creates an S3 Client

s3_client = boto3.client('s3')

try:

#Comment: This lists all S3 buckets in the AWS account and gets the list of bucket dictionaries.
    response = s3_client.list_buckets()
    buckets = response.get('Buckets', [])

    if not buckets:
        print("No S3 buckets found.")
    else:

#Comment: This iterates over each bucket in the S3 buckets, gets the name, and prints the name of the bucket.
        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"Bucket Name: {bucket_name}")

#Comment: This gets the public access block configuration for the current bucket, extracs the public access block settings,
#and loops through the public access block configuration. If none are configured, it will catch the error code and print it.
            
            try:
                public_access_block = s3_client.get_public_access_block(Bucket=bucket_name)
                config = public_access_block['PublicAccessBlockConfiguration']
                print("... Public Access Block Configuration:")
                for key, value in config.items():
                    print(f"... {key}: {value}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    print("... No Public Access Block Configuration.")
                else:
                    print(f"... Error getting public access block for bucket {bucket_name}: {e}")

#Comment: This section checks if the bucket has a policy attached. It will attempt to retrieve the bucket policy and handle the 
#case where there is no bucket policy and print any errors if they occur.

            try:
                policy = s3_client.get_bucket_policy(Bucket=bucket_name)
                print(" ... Bucket has a policy that might allow public access.")
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchBucketPolicy':
                    print ("... Bucket has no bucket policy.")
                else:
                    print(f"... Error getting bucket policy for bucket {bucket_name}: {e}")

#Comment: This checks the bucket's access control list to see who has access. It gets the list of permissions, iterates over the grants
#and checks if the bucket is publicly accessible and if the bucket is accessible to all authenticated AWS users.

            try:
                acl = s3_client.get_bucket_acl(Bucket=bucket_name)
                grants = acl.get('Grants', [])
                for grant in grants:
                    grantee = grant.get('Grantee', {})
                    permission = grant.get('Permission')

                    if grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/allUsers':
                        print(f"... Bucket is publicly accessible with permission: {permission}")
                    elif grantee.get('URI') == 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers':
                        print(f"... Bucket is accessible to all authenticaed AWS users with permission: {permission}")

            except ClientError as e:
                print(f"... Error getting ACL for bucket {bucket_name} {e}")

#Comment: adds a blank line between each bucket's output and except ClientError catches and prints general errors when listing buckets.
            print()

except ClientError as e:
    print(f"An Error occurred: [e]")

