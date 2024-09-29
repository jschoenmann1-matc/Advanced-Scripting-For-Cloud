#!/usr/bin/evn python3

#Comment: This imports essential services we need to run our script.
import boto3

#Comment: This creates an SNS topic with the given topic name in the stop or reboot script.
#This returns the Topic ARN, and that is returned to be able to manage later.
def CreateSNSTopic(topicName):
    sns_client = boto3.client('sns')

    response = sns_client.create_topic(Name=topicName)
    return response ['TopicArn']

#Comment: This function allows an email address to subscribe to an existing sns topic.
#It takes the Topic ARN and the email address and returns the subscription message which you confirm in the email.   
def SubscribeEmail(topicARN, emailAddress):
    sns_client = boto3.client('sns')
    response= sns_client.subscribe(TopicArn=topicARN, Protocol='email', Endpoint=emailAddress)
    return response['SubscriptionArn']