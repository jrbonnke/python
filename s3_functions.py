import boto3
import logging
from botocore.exceptions import ClientError
import os

REGIONS = ['us-east-2', 'us-west-2', 'ap-south-2', 'ap-south-1', 'ap-southeast-1']

def select_region():                                        #function for listing and selecting the region
    print("\nPlease select a region:")
    for idx, region in enumerate(REGIONS, 1):               #list out the region with index one by one it starts from 1
        print(f"{idx}. {region}")                           # print the regions in list


    choice = input("Enter the number of your choice: ")    # taking the input from the user
    try:
        choice = int(choice)                                #input is saved in choice variable as int
        if 1 <= choice <= len(REGIONS):                      #condition for checking whether value is there or not
            selected_region = REGIONS[choice - 1]              #if its available save the value in a variable  the list index starts from 0 so input has to be minized with 1
            print(f"Selected region: {selected_region}")       # print the selected region
            return selected_region                             #return the value that is been selected

        else:
            print("Invalid choice. Try again.")             
            return select_region()                             #invalid option 
    except ValueError:                                          #throw exception
        print("Invalid input. Please enter a number.")
        return select_region()                                  #again ask for selecting the input

def aws_region(region=None):                                    #fetching aws region details from the s3 client                        
    try:
        if region is None or region == "":                      #if there is no value it will take default region
            s3_client = boto3.client('s3')
        else:
            s3_client = boto3.client('s3', region_name=region)  # select the region which was given as input
    except ClientError as e:                                    # exception to handle error
        logging.error(e)
        return None
    
    return s3_client

def list_buckets(s3_client):                                   #function to list all the bucket details
    try:
        response = s3_client.list_buckets()                    #s3 client holds the region detail 
        buckets = response['Buckets']                          # the buck holds the complete buckrt details in specified region
        
        if not buckets:                                        # if ther are bucket throws null
            print("No buckets found.")
            return

        print("\nAvailable Buckets:")                           #else prints all the bucket details
        print("bucket name\t\t Created on ")            
        for bucket in buckets:                                             #lists bucket details one by one 
            print(f"- {bucket['Name']}\t\t ({bucket['CreationDate']})")    # prints
    except ClientError as e:                                               #catches error
        logging.error(e)

def create_bucket(s3_client, bucket_name, region):                  # creates new bucket           
    try:
        if region == 'us-east-1':                                      #if region is us-east-1 no need of location constrains
            s3_client.create_bucket(Bucket=bucket_name)                 #creates s3 bucket with the name passed.
        else:
            s3_client.create_bucket(                                   #if the region is not of us-east-1 then create bucket with location constrain by taking region
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region}
            )
        print(f"Bucket '{bucket_name}' created successfully.")
    except ClientError as e:
        logging.error(e)

def show_bucket_details(s3_client, bucket_name):                        #function to show bucket detail
    try:
        bucket_location = s3_client.get_bucket_location(Bucket=bucket_name) #get location
        print(f"Bucket Region: {bucket_location['LocationConstraint']}")   

        # policy = s3_client.get_bucket_policy(Bucket=bucket_name)            #policy
        # print(f"Bucket Policy: {policy['Policy']}")

        encryption = s3_client.get_bucket_encryption(Bucket=bucket_name)
        print(f"Encryption: {encryption['ServerSideEncryptionConfiguration']}")

        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        print(f"Versioning: {versioning}")

        # lifecycle = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        # print(f"Lifecycle Rules: {lifecycle['Rules']}")

       
        logging_conf = s3_client.get_bucket_logging(Bucket=bucket_name)
        print(f"Logging: {logging_conf.get('LoggingEnabled', 'No Logging Enabled')}")

        print("\nObjects in bucket:")
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"- {obj['Key']}")
        else:
            print("No objects in bucket.")
    except ClientError as e:
        logging.error(e)
        print("Some details my not be available or permissions are missing.")


def check_enable_versioning(s3_client, bucket_name):
    try:
        response = s3_client.get_bucket_versioning(Bucket=bucket_name)
        status = response.get('Status', 'Not Enabled')
        print(f"Versioning Status: {status}")

        if status != 'Enabled':
            choice = input("Versioning is not enabled. Enable now? (yes/no): ").lower()
            if choice == 'yes':
                s3_client.put_bucket_versioning(
                    Bucket=bucket_name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
                print("Versioning enabled successfully.")
    except ClientError as e:
        logging.error(e)

def upload_files(s3_client, bucket_name):
    folder_path = input("Enter folder path to upload files from: ").strip()

    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                s3_client.upload_file(file_path, bucket_name, filename)
                print(f"Uploaded: {filename}")
            except ClientError as e:
                logging.error(e)

def delete_bucket(s3_client, bucket_name):
    try:
        # First delete all objects
        print(f"Emptying bucket: {bucket_name}")
        objects = s3_client.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])
            print("All objects deleted.")

        # Now delete bucket
        s3_client.delete_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except ClientError as e:
        logging.error(e)

def main():
    logging.basicConfig(level=logging.ERROR)

    region = select_region()
    s3_client = aws_region(region)

    if not s3_client:
        print("Failed to create S3 client. Exiting...")
        return

    while True:
        print("\nOptions:")
        print("1. List Buckets")
        print("2. Create Bucket")
        print("3. Show Bucket Details")
        print("4. Check/Enable Versioning")
        print("5. Upload Files")
        print("6. Delete Bucket")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            list_buckets(s3_client)
        elif choice == '2':
            bucket_name = input("Enter new bucket name: ").strip()
            create_bucket(s3_client, bucket_name, region)
        elif choice == '3':
            bucket_name = input("Enter bucket name to view details: ").strip()
            show_bucket_details(s3_client, bucket_name)
        elif choice == '4':
            bucket_name = input("Enter bucket name for versioning check: ").strip()
            check_enable_versioning(s3_client, bucket_name)
        elif choice == '5':
            bucket_name = input("Enter bucket name to upload files: ").strip()
            upload_files(s3_client, bucket_name)
        elif choice == '6':
            bucket_name = input("Enter bucket name to delete: ").strip()
            delete_bucket(s3_client, bucket_name)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
