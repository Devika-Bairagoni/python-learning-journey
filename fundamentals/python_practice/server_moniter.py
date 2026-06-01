servers = [
    {"name": "api-server-01", "cpu": 45.6, "memory": 55.0},
    {"name": "db-server-01",  "cpu": 92.3, "memory": 87.3},
    {"name": "cache-01",      "cpu": 78.1, "memory": 94.1},
]


def monitor_all_servers(server_list):
    print("=" * 40)
    print("  SERVER HEALTH REPORT")
    print("=" * 40)
    for server in server_list:
        name   = server["name"]
        cpu    = server["cpu"]
        memory = server["memory"]

        if cpu > 80:
            cpu_status = "ALERT"
        elif cpu > 60:
            cpu_status = "WARNING"
        else:
            cpu_status = "OK"

        if memory > 90:
            mem_status = "ALERT"
        elif memory > 70:
            mem_status = "WARNING"
        else:
            mem_status = "OK"

        print(f"  {name}")
        print(f"    CPU    : {cpu}%  [{cpu_status}]")
        print(f"    Memory : {memory}%  [{mem_status}]")
    print("=" * 40)

monitor_all_servers(servers)