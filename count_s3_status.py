import boto3

# Create a session using AWS credentials (from AWS CLI or environment variables)
session = boto3.Session(region_name='eu-west-2')

# Create S3 client
s3_client = session.client('s3')

# List all S3 buckets
response = s3_client.list_buckets()

# Initialize count
total_buckets = 0

print("Listing all S3 buckets and their status:")

# Iterate through each bucket
for bucket in response['Buckets']:
    total_buckets += 1
    bucket_name = bucket['Name']
    print(f"Bucket Name: {bucket_name}")

    # Try to fetch the last modified object in the bucket
    try:
        # Paginate through all objects in the bucket
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name)
        last_modified = None

        for page in page_iterator:
            if 'Contents' in page:
                # Get the last modified date from the current page of objects
                page_last_modified = max(obj['LastModified'] for obj in page['Contents'])
                if last_modified is None or page_last_modified > last_modified:
                    last_modified = page_last_modified

        if last_modified:
            print(f"  - Last modified date of objects: {last_modified}")
        else:
            print("  - No objects found in the bucket")
    except Exception as e:
        print(f"  - Could not retrieve objects due to: {str(e)}")

print(f"Total number of S3 buckets: {total_buckets}")
