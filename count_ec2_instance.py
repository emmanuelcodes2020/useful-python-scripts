import boto3

# Create a session using your AWS credentials (not needed if using AWS CLI config)
# session = boto3.Session(
#     aws_access_key_id='YOUR_ACCESS_KEY',
#     aws_secret_access_key='YOUR_SECRET_KEY',
#     region_name='us-west-2'  # Specify your region
# )

# Create EC2 client
ec2_client = boto3.client('ec2')

# Get information about all instances
response = ec2_client.describe_instances()

# Initialize count
total_instances = 0

# Iterate through instances
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        total_instances += 1
        print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")

print(f"Total number of EC2 instances: {total_instances}")
