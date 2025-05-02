import boto3
ec2 = boto3.client('ec2')
response = ec2.describe_instance(
    Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running', 'stopped']
            }
        ]
)
print(response)