servers = [
    {"name": "api-server-01", "cpu": 45.6, "memory": 55.0, "region": "us-east-1"},
    {"name": "db-server-01",  "cpu": 92.3, "memory": 87.3, "region": "us-east-1"},
    {"name": "cache-01",      "cpu": 78.1, "memory": 94.1, "region": "us-west-2"},
    {"name": "api-server-02", "cpu": 12.4, "memory": 34.2, "region": "us-west-2"},
]

# Build a lookup dictionary - name becomes the key
server_lookup = {}

for server in servers:
    server_lookup[server["name"]] = server


result = server_lookup.get("ghost-server")
print(result)

result2 = server_lookup.get("ghost-server", "Server not found")
print(result2)