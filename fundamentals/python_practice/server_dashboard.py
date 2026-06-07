servers = [
    {"name": "api-server-01", "cpu": 45.6, "memory": 55.0, "status": "running"},
    {"name": "db-server-01",  "cpu": 92.3, "memory": 87.3, "status": "running"},
    {"name": "cache-01",      "cpu": 78.1, "memory": 94.1, "status": "running"},
    {"name": "api-server-02", "cpu": 12.4, "memory": 34.2, "status": "running"},
    {"name": "backup-01",     "cpu": 5.1,  "memory": 22.0, "status": "stopped"},
]

def get_health_status(cpu, memory):
    if cpu > 80 or memory > 90:
        return "CRITICAL"
    elif cpu > 60 or memory > 70:
        return "WARNING"
    else:
        return "HEALTHY"
 

def server_dashboard(server_list):
    print("=" * 50)
    print("       SERVER DASHBOARD")
    print("=" * 50)
    
    for server in server_list:
        status = get_health_status(server["cpu"], server["memory"])
        print(f"  {server['name']:<20} {server['status']:<10} CPU:{server['cpu']}%  MEM:{server['memory']}%  [{status}]")
        total = len(server_list)
    critical = 0
    healthy = 0

    for server in server_list:
        status = get_health_status(server["cpu"], server["memory"])
        if status == "CRITICAL":
            critical += 1
        else:
            healthy += 1

    print(f"  Total: {total}  Healthy: {healthy}  Critical: {critical}")
    
    print("=" * 50)

server_dashboard(servers)
