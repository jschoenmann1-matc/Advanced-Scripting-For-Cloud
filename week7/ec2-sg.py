#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: This script audits EC2 security groups to check for open inbound rules that could expose resources
#to the public internet. This lists security group names, inbound rules, and warns if any rules allow access to the public.

import boto3
import argparse
from botocore.exceptions import ClientError

#Comment: This creates an EC2 Client

ec2_client = boto3.client('ec2')

#Comment: This sets up argument parsing for the script and allows user to input a security group name as an argument.

parser = argparse.ArgumentParser(description= 'Check security groups for open access.')
parser.add_argument('-s', '--security-group', help='Named of the security group to check', required=False)
args = parser.parse_args()

#Comment: This fucntion checks a security group's inbound rules. Gets the security group name and ID, and prints it.

def check_security_group(sg):
    sg_name = sg.get('GroupName', 'Unnamed')
    sg_id = sg.get('GroupId', 'Unknown')
    print(f"Security Group: {sg_name} ({sg_id})")

    permissions = sg.get('IpPermissions', [])

#Comment: If no inbound rules are found this indicates that the security group has no inbound rules. This also gets the list of all IPv4 and IPv6 ranges allowed by this role.
#ip_range checks the IPv4 and IPv6 ranges for public access by getting the CIDR for both.
    if not permissions:
        print("... No inbound rules.")
    else:
        for perm in permissions:
            from_port = perm.get('FromPort', 'All')
            to_port = perm.get('ToPort', 'All')
            ip_protocol = perm.get('IpProtocol', 'All')
            ip_ranges = perm.get('IpRanges', [])
            ipv6_ranges = perm.get('Ipv6Ranges', [])

            for ip_range in ip_ranges:
                cidr = ip_range.get('CidrIp', '')
                if cidr == '0.0.0.0/0':
                    print(f"... Protocol: {ip_protocol}, Ports: {from_port}-{to_port}, CIDR: {cidr}")
                    print(f"... WARNING: This is open to the public internet!")
                else:
                    print(f"... Protocol: {ip_protocol}, Ports: {from_port}-{to_port}, CIDR: {cidr}")
            
            for ipv6_ranges in ipv6_ranges:
                cidr_ipv6 = ipv6_range.get('CidrIpv6', '')
                if cidr_ipv6 == '::/0':
                    print(f"... Protocol: {ip_protocol}, Ports: {from_port}-{to_port}, CIDR: {cidr_ipv6}")
                    print(f"... WARNING: This is open to the public internet!")
                else:
                    print(f"... Protocol: {ip_protocol}, Ports: {from_port}-{to_port}, CIDR: {cidr_ipv6}")

    print()

#Comment: If the user provided a specific security group name, it will filter ther request by that security group.
#if no secuirty groups are found, a message will be printed and iterated over each security group.
try:
    if args.security_group:
        response = ec2_client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [args.security_group]
                }
            ]
        )
    else:
        response = ec2_client.describe_security_groups()

    security_groups = response['SecurityGroups']

    if not security_groups:
        print("No security groups found.")
    else:
        for sg in security_groups:
            check_security_group(sg)

#Comment: This prints any errors that occure when interacting with AWS EC2 services.

except ClientError as e:
    print(f"An error occured: {e}")
