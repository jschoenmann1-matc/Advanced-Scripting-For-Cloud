#!/usr/bin/env python3

#Comment: This imports essential services we need to run our script.
import boto3
import ec2
import sns

#Comment: This allows us to set true or false to test our script without actually executing it.
DRYRUN = False

#Comment: This creates a client to get the account ID.
sts_client = boto3.client("sts")

account_id = sts_client.get_caller_identity()["Account"]

#Comment: This creates an EC2 client and gets the most recent AMI ID.
ec2_client = boto3.client('ec2')

image = ec2.Get_Image(ec2_client)

#Comment: This launches the EC2 instance with the ID.
instance = ec2.Create_EC2(image,ec2_client)

#Comment: This sets up a CloudWatch client for monitoring.
cwclient = boto3.client('cloudwatch')

#Comment: This creates an SNS topic and an email to receive alarm notifications.
topicARN = sns.CreateSNSTopic('JordanExampleTopic')
subscriptionARN = sns.SubscribeEmail(topicARN, 'jschoenmann1@madisoncollege.edu')

#Comment: This creates a CloudWatch alarm that monitors CPU utilization of our EC2 instance.
#If the CPU usage is above 70% for two 5-minute periods, the alarm will be set to In Alarm.
#When the alarm triggers, the EC2 instance stops and the notification to the administrator is sent.
response = cwclient.put_metric_alarm(
    AlarmName='Web_Server_HIGH_CPU_Utilization',
    ComparisonOperator='GreaterThanOrEqualToThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=70.0,
    ActionsEnabled=True,
    AlarmActions=[
        f'arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Reboot/1.0',
        f'arn:aws:sns:us-east-1:{account_id}:JordanExampleTopic'
    ],
    AlarmDescription='Alarm when server CPU exceeds 70%',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance
        },
    ]

)