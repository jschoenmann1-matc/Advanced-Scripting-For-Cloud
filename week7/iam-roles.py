#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script uses Boto3 to audit IAM roles created in the last 90 days. This lists both managed and inline policies associated with each role.
#It includes error handling for permissions and outputs clear messages for accessed denied policies.

import boto3
import datetime
import pytz
from botocore.exceptions import ClientError

#Comment: This creates an IAM Client

iam_client = boto3.client('iam')

#Comment: This gets the current UTC time

current_time = pytz.utc.localize(datetime.datetime.utcnow())

#Comment: This calculates the time 90 days ago from today.

time_90_days_ago = current_time - datetime.timedelta(days=90)

try:

#Comment: Paginator is used to handle the roles if there are too many. It then gets looped through each of the roles and the role name and creation date are extracted.
    paginator = iam_client.get_paginator('list_roles')
    for page in paginator.paginate():
        for role in page['Roles']:
            role_name = role['RoleName']
            role_creation_date = role['CreateDate']

#Comment: This only will list roles in the last 90 days.
            if role_creation_date > time_90_days_ago:
                print(f"Role Name: {role_name} - Created: {role_creation_date}")

#Comment: This grabs the attached managed policies for this role and lists them. If the managed policies are attached it will print each one.
#Otherwise, it will print error messages for access denial or something else.

                try:
                    attached_policies_response = iam_client.list_attached_role_policies(RoleName=role_name)
                    attached_policies = attached_policies_response['AttachedPolicies']
                    if attached_policies:
                        print("Attached Managed Policies")
                        for policy in attached_policies:
                            print(f"... has managed policy name: {policy['PolicyName']}")
                    else:
                        print("... No Managed policies attached.")
                except ClientError as e:
                    if e.response['Error']['Code'] == 'AccessDenied':
                        print(f"... Access Denied: You do not have permission to view the managed policies for role {role_name}.")
                    else:
                        print (f"... Could not retrieve attached managed polcies for role {role_name}. Error: {e}")

#Comment: This grabs the attached inline policies for this role and lists them. If the inline policies are attached it will print each one.
#Otherwise, it will print error messages for access denial or something else.

                try:
                    inline_policies_response = iam_client.list_role_policies(RoleName=role_name)
                    inline_policies = inline_policies_response['PolicyNames']
                    if inline_policies:
                        for policy_name in inline_policies:
                            print(f"... has unmanaged polciy name:{policy_name}")
                    else:
                        print ("... No unmanaged policies attached.")
                except ClientError as e:
                    if e.response['Error']['Code'] == 'AccessDenied':
                        print(f"... Access Denied: You do not have permission to view the inline policies for role {role_name}.")
                    else:
                        print(f"... Could not retrieve inline policies for role {role_name}. Error: {e}")

                print()

#Comment: This is an error handler for issues that aren't related to policy access.

except ClientError as e:
    print(f"An Error Occured: {e}")