import boto3
from datetime import datetime

# Create a session using AWS credentials (from AWS CLI or environment variables)
session = boto3.Session(region_name='eu-west-2')

# Create ACM client for certificate monitoring
acm_client = session.client('acm')

# Get current time for comparison
current_time = datetime.now()

# List ACM certificates (with pagination)
print("\nListing all ACM certificates and their details:")
next_token = None
total_certificates = 0

while True:
    if next_token:
        certificates = acm_client.list_certificates(NextToken=next_token)
    else:
        certificates = acm_client.list_certificates()

    if not certificates['CertificateSummaryList']:
        print("No ACM certificates found.")
        break

    # Iterate over the list of certificates
    for cert in certificates['CertificateSummaryList']:
        cert_arn = cert['CertificateArn']
        cert_details = acm_client.describe_certificate(CertificateArn=cert_arn)
        
        cert_domain = cert_details['Certificate']['DomainName']
        cert_status = cert_details['Certificate']['Status']
        cert_expiration = cert_details['Certificate']['NotAfter']
        

        # Calculate days left until expiration
        #days_to_expire = (cert_expiration - current_time).days

        # Print certificate details
        print(f"\nCertificate Domain: {cert_domain}")
        print(f"  Status: {cert_status}")
        print(f"  Expiration Date: {cert_expiration}")
        #print(f"  Days to Expire: {days_to_expire} days")

        total_certificates += 1

    next_token = certificates.get('NextToken')
    if not next_token:
        break

if total_certificates == 0:
    print("No ACM certificates found.")
else:
    print(f"\nTotal number of ACM certificates: {total_certificates}")
