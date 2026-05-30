# A list of servers
# Each server is a dictionary with name, cpu, and memory

servers = [
    {"name": "api-server-01", "cpu": 45.6, "memory": 55.0},
    {"name": "db-server-01",  "cpu": 92.3, "memory": 87.3},
    {"name": "cache-01",      "cpu": 78.1, "memory": 94.1},
]

# Loop through each server and print its name
for server in servers:
    print(server["name"])

# Loop through and print cpu of each server
for server in servers:
    print(f"{server['name']} - CPU: {server['cpu']}%")

# Loop through and print memory of each server
for server in servers:
    if server["cpu"] > 80:
        print(f"ALERT: {server['name']}")
    elif server["cpu"] > 60:
        print(f"WARNING: {server['name']}")
    else:
        print(f"OK: {server['name']}")