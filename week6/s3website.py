#!/usr/bin/env python3
#Author: Jordan Sexton-Schoenmann

#General Description: This script will set up an s3 bucket to act as a static website. It creates a bucket and applies policy to make it readable
#configure it to serve web pages, and uploads two HTML files to the bucket.


#Comment: This loads boto3 and json for working with AWS and json data.
#Also imports modules for random string generation, arguement parsing, and handling exceptions with botocore.

import boto3,json

import random,argparse,string,botocore

#Comment: This sets up the s3 client to work with AWS and bucket_name defines the new bucket name with bucket response creating it.
#Parser sets up arguement parsing to allow the user to supply a custom name and randomly generates one if none is supplied with a suffix.

s3client = boto3.client('s3')

bucket_name = "sextonschoen-script2-week2-f24"

parser = argparse.ArgumentParser(description="Arguments to supply bucket name for our s3website")
parser.add_argument('-s','--sitename',dest='site_name',default='', type=str, help='Enter a unique bucket name for your s3website')
args = parser.parse_args()

if not args.site_name:
    print(f"No site_name was provided, we will use a random generator")
    bucket_name += "".join(random.choices(string.ascii_lowercase, k=10))
else:
    print(f"You specified a bucket name of {args.site_name}.")
    bucket_name = args.site_name

#Comment: This creates a new bucket using the generated or provided name and removes the public access block for this bucket.

try:
    bucket_response = s3client.create_bucket(Bucket=bucket_name)

    s3client.delete_public_access_block(Bucket=bucket_name)

#Comment: This defines and applies policies to allow public read access.It then converts the bucket policy dictionary to a JSON string for AWS
#and applies the bucket policy to enable public read access.

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

    response = s3client.put_bucket_policy(
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

#Comment: This handles cases where AWS credentials are invalid or expired and prompt the user to update them.
#It also handles any other AWS client errors and provides details to help troubleshoot including the specific case where the bucket name already exists in AWS.

except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] =='InvalidToken':
        print("Please update your aws credentials with a valid token")
    else:
        print(f"Some other error occured {error}")
except client.meta.client.exceptions.BucketAlreadyExists as err:
    print("Bucket {} already exists!".format(err.response['Error']['BucketName']))
    print("Re-run the script with a valid bucket name")