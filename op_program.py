import random

servers = ['server1' 'server2' 'server3' 'server3']

success_count = 0
failure_count = 0

for server in servers:
    ping_success = random.choice([True,False])

    if ping_success:
        print(f"{server} is up")
        success_count += 1
    
    else:
        print(f"{server} is DOWN")
        failure_count += 1
        
print("\nSummary:")
print(f"Total Servers Checked: {len(servers)}")
print(f"Successful: {success_count}")
print(f"Failed: {failure_count}")
