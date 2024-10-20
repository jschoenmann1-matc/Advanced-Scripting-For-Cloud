#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script uses Boto3 to manage an Amazon S3 bucket. It has functions to create a new S3 bucket, delete the bucket,
#enable versioning, and set the bucket policy. 

import boto3

#Comment: This creates and S3 bucket and initializes it and returns the response from AWS.

def CreateBucket(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.create_bucket(Bucket=bucket_name)
    return response

#Comment: This deletes an S3 bucket and returns the response from AWS.

def DeleteBucket(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.create_bucket(Bucket=bucket_name)
    return response

#Comment: This enforces versioning on the S3 bucket. It initializes an S3 client and enables versioning on the bucket with a specific configuration.

def EnforceVersioning(bucket_name):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={
            'MFADelete': 'Disabled',
            'Status': 'Enabled',
        }
    )
    return response

#Comment: This sets a policy on the S3 bucket and provides a policy to the bucket.

def SetBucketPolicy(bucket_name, policy):
    s3client = boto3.client('s3')
    response = s3client.put_bucket_policy(Bucket = bucket_name, Policy=policy)
    return response

#Comment: This function does the creation and versioning of the S3 bucket. It calls createbucket to create the S3 bucket and enforceversioning to 
#enable versioning on the S3 bucket.

def main():
    bucket_name = "jordanschoenmann-demo-v1"
    response = CreateBucket(bucket_name)
    version_response = EnforceVersioning(bucket_name)

if __name__ == "__main__":
    main()
