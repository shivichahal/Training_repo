import boto3
import json
import yaml
from botocore.exceptions import ClientError

# Initialize the S3 client using your local AWS credentials
s3 = boto3.client('s3')

# Configuration Variables
BUCKET_NAME = "oubt-dev-us-east-2-data-lake"
REGION = "us-east-2"


# Creating Bucket
def create_bucket():
    try:
        if REGION == 'us-east-1':
            s3.create_bucket(Bucket=BUCKET_NAME)
        else:
            s3.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={'LocationConstraint': REGION}
            )
        print(f" Bucket '{BUCKET_NAME}' created successfully.")
    except ClientError as e:
        print(f" Error creating bucket: {e}")

    # security policies
def set_security_controls():
    s3.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
    print(" Public Access Blocked.")

    # setting lifecycle
def set_lifecycle_policy():
    lifecycle_config = {
        'Rules': [
            {
                'ID': 'ArchiveOldData',
                'Status': 'Enabled',
                'Filter': {'Prefix': 'archive/'},
                'Transitions': [
                    {'Days': 90, 'StorageClass': 'GLACIER'}
                ]
            }
        ]
    }
    s3.put_bucket_lifecycle_configuration(
        Bucket=BUCKET_NAME, 
        LifecycleConfiguration=lifecycle_config
    )
    print(" Lifecycle policy applied (Archive to Glacier after 90 days).")

    #Uploading Data with Prefixes and Tags
def upload_with_governance(local_path, s3_key):
    # Governance tags
    tags = "Owner=DataEngineering&Classification=Internal&Domain=Analytics"
    
    try:
        s3.upload_file(
            local_path, 
            BUCKET_NAME, 
            s3_key, 
            ExtraArgs={'Tagging': tags}
        )
        print(f" File {s3_key} uploaded with metadata tags.")
    except FileNotFoundError:
        print(" Local file not found.")

    #Generating the Metadata Manifest
def create_manifest():
    manifest_data = {
        "bucket_info": {
            "name": BUCKET_NAME,
            "region": REGION,
            "ownership": "Data Platform Team",
            "data_classification": "Confidential",
            "description": "Storage for raw financial ingestion pipelines"
        }
    }
    
    with open('bucket_manifest.yaml', 'w') as f:
        yaml.dump(manifest_data, f, sort_keys=False)
    print("Documentation manifest 'bucket_manifest.yaml' created.")

    #Execution Logic

if __name__ == "__main__":
    # 1. Create
    create_bucket()
    
    # 2. Secure
    set_security_controls()
    
    # 3. Automate
    set_lifecycle_policy()
    
    # 4. Upload & Tag (Organizing with 'raw/2025/' prefix)
    # Ensure you have a file named 'data.txt' locally to test this
    upload_with_governance('taxi_zone_lookup.csv', 'raw/test/taxi_zone_lookup.csv')
    
    # 5. Document
    create_manifest()

