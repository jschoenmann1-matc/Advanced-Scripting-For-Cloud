#!/usr/bin/env python3
#Author: Jordan Sexton-Schoenmann

#General Description: This script will set up an s3 bucket to act as a static website. It creates a bucket and applies policy to make it readable
#configure it to serve web pages, and uploads two HTML files to the bucket.


#Comment: This loads boto3 and json for working with AWS and json data.
import boto3,json


#Comment: This sets up the s3 client to work with AWS and bucket_name defines the new bucket name with bucket response creating it.
s3client = boto3.client('s3')

bucket_name = "sextonschoen-script2-week2-f24"

bucket_response = s3client.create_bucket(Bucket=bucket_name)


#Comment: This defines and applies policies to allow public read access.
bucket_policy = {
    'Version': '2012-10-17',
    'Statement': [{
        'Sid': 'AddPerm',
        'Effect': 'Allow',
        'Principal': '*',
        'Action': ['s3:GetObject'],
        'Resource': "arn:aws:s3:::%s/*" % bucket_name
     }]
}

bucket_policy_string = json.dumps(bucket_policy)

bucket_policy_response = s3client.put_bucket_policy(
    Bucket=bucket_name,
    Policy=bucket_policy_string
)


#Comment: This sets up the bucket to serve static website files.
put_bucket_response = s3client.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
    'ErrorDocument': {'Key': 'error.html'},
    'IndexDocument': {'Suffix': 'index.html'},
    }
)


#Comment: This uploads the index and error html files to the bucket for the website.
indexFile = open('index.html', 'rb')
put_index_response = s3client.put_object(Body=indexFile, Bucket=bucket_name, Key='index.html' ,ContentType='text/html')
indexFile.close()
print(put_index_response)

errorFile = open('error.html', 'rb')
put_index_response = s3client.put_object(Body=errorFile, Bucket=bucket_name, Key='error.html' ,ContentType='text/html')
errorFile.close()
print(put_index_response)