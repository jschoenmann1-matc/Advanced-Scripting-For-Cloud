import boto3

#Comment: Create a session and EC2 client

session = boto3.Session()
ec2_client = session.client('ec2')

def list_instances_and_check_sg():

#Comment: Get all EC2 instances and check their security groups.

    print("Fetching EC2 instances...")
    instances = ec2_client.describe_instances()
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            print(f"Instance ID: {instance_id}")
            
#Comment: Check the security groups attached to the instance.

            security_groups = instance.get('SecurityGroups', [])
            for sg in security_groups:
                sg_id = sg['GroupId']
                sg_name = sg['GroupName']
                print(f"  Security Group ID: {sg_id}, Name: {sg_name}")
                check_and_revoke_sg_rules(sg_id)

def check_and_revoke_sg_rules(sg_id):

#Comment: Describe the security group and revoke security group ingress rules for port 22. Gets all the ingress rules for the security group.
#Revokes the rule if it allows access from 0.0.0.0/0 and exits loop.

    response = ec2_client.describe_security_groups(GroupIds=[sg_id])
    security_group = response['SecurityGroups'][0]
    
    ingress_rules = security_group.get('IpPermissions', [])
    for rule in ingress_rules:
        if rule.get('IpProtocol') == 'tcp' and rule.get('FromPort') == 22 and rule.get('ToPort') == 22:
            print(f"    Found ingress rule for port 22 in Security Group {sg_id}. Checking CIDRs...")
            revoke_needed = False
            for ip_range in rule.get('IpRanges', []):
                cidr = ip_range.get('CidrIp')
                if cidr == '0.0.0.0/0':
                    revoke_needed = True
                    print(f"    Rule allows access from {cidr}. Revoking access...")
                    revoke_ingress_rule(sg_id, rule)
                    break
            
            if not revoke_needed:
                print("    No action needed. Port 22 is restricted.")

#Comment: This portion revokes a specific ingress rule from a security group.

def revoke_ingress_rule(sg_id, rule):
    try:
        ec2_client.revoke_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': rule['IpProtocol'],
                    'FromPort': rule['FromPort'],
                    'ToPort': rule['ToPort'],
                    'IpRanges': rule['IpRanges']
                }
            ]
        )
        print(f"    Successfully revoked ingress rule for Security Group {sg_id}.")
    except Exception as e:
        print(f"    Error revoking rule for Security Group {sg_id}: {e}")

if __name__ == "__main__":
    print("Starting Security Group Monitoring...")
    list_instances_and_check_sg()
    print("Monitoring complete.")
