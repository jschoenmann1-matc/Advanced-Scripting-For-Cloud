#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script sets up an AWS CloudTrail to log activity to a specific S3 Bucket and applies policy to the bucket to allow CloudTrail access.
#This script also handles things where the trail already exists and starts logging on the existing trail. 

import boto3,s3enforce,json 

#Comment: This creats a cloudtrail with the specific name and bucket. If this cloudtrail already exists, it starts logging for that cloudtrail.

def CreateTrail(trail_name, bucket_name):
    trailclient = boto3.client('cloudtrail')
    try:
        response = trailclient.create_trail(S3BucketName=bucket_name, Name=trail_name)
        return response
    except trailclient.exceptions.TrailAlreadyExistsException as error:
        response = trailclient.start_logging(Name=trail_name)
        return response

#Comment: The main function creates the bucket, applies the policy, and creates the CloudTrail. It starts the client and gets the ID for use in the policy.
#This also defines bucket and trail names and defines the bucket policy that allows cloudtrail to access the bucket.

def main ():
    sts_client = boto3.client("sts")
    account_id = sts_client.get_caller_identity()["Account"]

    bucket_name = "jordan1-cloud-trail-demo"
    trail_name = "jordan1-schoenmann-ct-demo"
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }

#Comment: This applies the policy to the bucket using the SetBucketPolicy function.
    response = s3enforce.CreateBucket(bucket_name)
    policy_response = s3enforce.SetBucketPolicy(bucket_name, json.dumps(policy))

#Comment: This creates the CloudTrail and associates it with the S3 bucket and prints the responses for visibility.
    response = CreateTrail(trail_name, bucket_name)
    print(response)

if __name__ == "__main__":
    main()