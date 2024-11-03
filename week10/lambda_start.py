#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script creates and invokes a Lambda function that stops EC2 instances using the function StartEC2.
import boto3

#Comment: This initalizes the Lambda and IAM Clients.

lambda_client = boto3.client('lambda')
iam = boto3.client('iam')

#Comment: This creates a Lambda function using an existing role and and a zip file containing the function code.It retrieves the ARN for the role assigned to the function.
#It also opens the zip file containing the Lambda function.

def Create_Lambda(function_name):
    role_response = iam.get_role(RoleName='LabRole')
    handler = open('lambda_start_function.zip','rb')
    zipped_code = handler.read()

#Comment: This creates the function with the necessary parameters and config setup.

    response = lambda_client.create_function(
        FunctionName = function_name,
        Role = role_response['Role']['Arn'],
        Publish = True,
        PackageType = 'Zip',
        Runtime = 'python3.9',
        Code={
            'ZipFile': zipped_code
        },
        Handler='lambda_start_function.lambda_handler'

    )

#Comment: This allows the lambda function to be invoked by name and return its response.

def Invoke_Lambda(function_name):
    invoke_response = lambda_client.invoke(FunctionName = function_name)
    return invoke_response

#Comment: The main function checks if the Lambda function exists and creates it if necessary. Then invokes it.

def main():
    functionName = 'startEC2'
    try:
        function = lambda_client.get_function(FunctionName=functionName)
        print("Function Already Exists")
    except:
        print("Creating Function")
        response = Create_Lambda(functionName)
        
    print("Invoking Lambda Function")
    Invoke_Lambda(functionName)


if __name__ == "__main__":
    main()
