import boto3

ec2_client = boto3.client('ec2', region_name='us-east-1')

instance_ids = ['i-0fa8672b76a95fd4d']  

def stop_instances():
    print(f"Stopping instances: {instance_ids}")
    response = ec2_client.stop_instances(InstanceIds=instance_ids)
    for instance in response['StoppingInstances']:
        print(f"Instance {instance['InstanceId']} state: {instance['PreviousState']['Name']} → {instance['CurrentState']['Name']}")

def start_instances():
    print(f"Starting instances: {instance_ids}")
    response = ec2_client.start_instances(InstanceIds=instance_ids)
    for instance in response['StartingInstances']:
        print(f"Instance {instance['InstanceId']} state: {instance['PreviousState']['Name']} → {instance['CurrentState']['Name']}")




def main():

    while True:
        print("\nOptions:")
        print("1. start instance")
        print("2. stop instance")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            start_instances()
        elif choice == '2':
            stop_instances()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

