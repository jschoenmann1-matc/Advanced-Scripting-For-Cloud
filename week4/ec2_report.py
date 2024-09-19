#!/usr/bin/env python3

#Author: Jordan Sexton-Schoenmann

#General Description: The script retrieves information about running Amazon EC2 instances which includes instance IDs, types, states, public IPs,
#monitoring states, and instance names. Then it writes the data to both a CSV and a text file.

import boto3,csv,json

#Comment: This section gets a list of EC2 instances based on the filter. It then uses pagination to ensure all instances are captured.
#Then, it returns a list of instances with details like instance ID, type, state, public IP.

def Get_Instances(filter_name='instance-state-name', filter_values=['running']):
    ec2_client = boto3.client('ec2')
    paginator =ec2_client.get_paginator('describe_instances')
    page_list = paginator.paginate(
        Filters=[
            {
	            'Name': filter_name,
	            'Values': filter_values,
	        },
        ]
    )

#Comment:This section extracts the information from the instances and handles missing attributes.

    response = []
    for page in page_list:
        for reservation in page['Reservations']:
            for instance in reservation['Instances']:
                instance_info = {
                    "InstanceId": instance['InstanceId'],
                    "InstanceType": instance['InstanceType'],
                    "State": instance['State']['Name'],
                    "PublicIpAddress": instance.get('PublicIpAddress', 'N/A') if 'PublicIpAddress' in instance else 'N/A',
                    "MonitoringState": instance['Monitoring']['State'],
                    "InstanceName": next(
                        (tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), 'N/A'
                    )
                }
                response.append(instance_info)
    return response


#Comment: This writes the instance data to a CSV file. The header arguement defines the column names and contents contains the data.
#If there are any errors, it will print them to the console.

def CSV_Writer(header, content):
    try:
        with open('export.csv', 'w', newline='') as hFile:
            writer = csv.DictWriter(hFile, fieldnames=header)
            writer.writeheader()
            for line in content:
                writer.writerow(line)
    except Exception as e:
        print("Error during CSV writing:", e)

#Comment: This section retrives the EC2 instances and the gathering of instance data. It then saves and formats it to both a CSV and a text file. 

def main():

    response = Get_Instances('instance-state-name', ['running'])
    headerRow = ['InstanceId','InstanceType','State','PublicIpAddress','MonitoringState','InstanceName']
    CSV_Writer(headerRow,response)

    with open('ec2_report_output.txt', 'w') as outfile:
        for item in response:
            outfile.write(json.dumps(item, indent=4) + "\n")


if __name__ == "__main__":
    main()



























    #print(type(response))
    #for instance in response:
        #for ec2 in instance['Instances']:
            #print(ec2['InstanceId'])
            #content.append(
                #{
                    #"InstanceId": ec2['InstanceId'],
                   # "InstanceType": ec2['InstanceType'],
                    #"State": ec2['State']['Name'],
                    #"PublicIpAddress": ec2.get('PublicIpAddress',"N/A")
                #}

            #)
    #CSV_Writer(headerRow,content)