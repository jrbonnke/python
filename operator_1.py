
#Arthematic operator 
total_clients = 440
servers_needed = total_clients // 100 + (1 if total_clients % 100 else 0)
print(servers_needed)

#comparision operator
disk_usage = 85
if disk_usage > 80:
    print("Warning: Disk space critical!")

cpu_load =70
if disk_usage > 80 or cpu_load >85:
    print("restart the server")