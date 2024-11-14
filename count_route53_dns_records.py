import boto3

# Create a session using AWS credentials (from AWS CLI or environment variables)
session = boto3.Session(region_name='eu-west-2')

# Create Route53 client
route53_client = session.client('route53')

# Get list of hosted zones
hosted_zones = route53_client.list_hosted_zones()

total_records = 0

# Iterate through each hosted zone to count DNS records
for zone in hosted_zones['HostedZones']:
    zone_id = zone['Id']
    print(f"Processing Hosted Zone ID: {zone_id}")

    # Initialize record count for the current hosted zone
    zone_record_count = 0
    is_truncated = True
    next_record_name = None

    # Paginate through record sets if needed
    while is_truncated:
        if next_record_name:
            response = route53_client.list_resource_record_sets(
                HostedZoneId=zone_id,
                StartRecordName=next_record_name
            )
        else:
            response = route53_client.list_resource_record_sets(
                HostedZoneId=zone_id
            )

        # Add the count of current records to the zone count
        zone_record_count += len(response['ResourceRecordSets'])

        # Check if response is truncated (more records to retrieve)
        is_truncated = response.get('IsTruncated', False)
        if is_truncated:
            next_record_name = response['NextRecordName']

    total_records += zone_record_count
    print(f"Hosted Zone ID: {zone_id}, Record count: {zone_record_count}")

print(f"Total number of Route53 records: {total_records}")
