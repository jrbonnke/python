import boto3
import logging
from botocore.exceptions import ClientError

REGIONS = ['us-east-2','us-west-2','ap-south-2','ap-south-1','ap-southeast-1']

def create_bucket(bucket_name, region = None):
    try:
        if region is None or region == "":
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
             s3_client = boto3.client('s3', region_name=region)
             location = {'LocationConstraint': region}
             s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration=location
            )
    except ClientError as e:
        logging.error(e)
        return False
    return True

if __name__ == "__main__":
    bucket_name = input("enter unique bucket name:").strip()

    print("\nChoose a region:")
    for idx, region_option in enumerate(REGIONS, start=1):
        print(f"{idx}. {region_option}")

    region_choice = input("Enter the number of the region (or press Enter for default us-east-1): ").strip()

    if region_choice == "":
        region = None  # Default will be handled in create_bucket
    else:
        try:
            region_index = int(region_choice) - 1
            if 0 <= region_index < len(REGIONS):
                region = REGIONS[region_index]
            else:
                print("Invalid choice. Using default region (us-east-1).")
                region = None
        except ValueError:
            print("Invalid input. Using default region (us-east-1).")
            region = None

    success = create_bucket(bucket_name, region)

    if success:
        print(f"Bucket '{bucket_name}' created successfully!")
    else:
        print(f"Failed to create bucket '{bucket_name}'.")
