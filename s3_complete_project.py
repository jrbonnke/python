import boto3
import logging
import os
from botocore.exceptions import ClientError

REGIONS = ['us-east-2', 'us-west-2', 'ap-south-2', 'ap-south-1', 'ap-southeast-1']

def select_region():
    print("\nPlease select an AWS region:")
    for idx, region in enumerate(REGIONS, 1):
        print(f"{idx}. {region}")
    
    choice = input(f"Enter the number of your choice (default is 1): ").strip()

    if not choice:  # User pressed Enter
        selected_region = REGIONS[0]
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(REGIONS):
                selected_region = REGIONS[choice - 1]
            else:
                print("Invalid choice. Using default region.")
                selected_region = REGIONS[0]
        except ValueError:
            print("Invalid input. Using default region.")
            selected_region = REGIONS[0]

    print(f"✅ Selected region: {selected_region}")
    return selected_region