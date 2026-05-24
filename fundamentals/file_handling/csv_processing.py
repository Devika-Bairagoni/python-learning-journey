import csv
from pathlib import Path

print("=== Writing CSV ===")
output_path = Path("fundamentals/file_handling/servers.csv")
headers = ["server_id", "name", "region", "status", "cpu_usage"]
rows = [
    ["srv-001", "api-server-01", "us-east-1", "running",  45.2],
    ["srv-002", "db-server-01",  "us-east-1", "running",  78.9],
    ["srv-003", "cache-01",      "us-west-2", "degraded", 91.3],
    ["srv-004", "api-server-02", "us-west-2", "stopped",   0.0],
]
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
print(f"  Written: {output_path}")

print("\n=== Reading CSV ===")
with open(output_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    servers = [row for row in reader]
print(f"  Loaded {len(servers)} servers")
for server in servers:
    print(f"  {server['server_id']} | {server['name']} | {server['status']}")

print("\n=== Processing CSV Data ===")
for server in servers:
    server["cpu_usage"] = float(server["cpu_usage"])
high_cpu = [s for s in servers if s["cpu_usage"] > 80]
print(f"  High CPU servers: {len(high_cpu)}")
for s in high_cpu:
    print(f"    {s['name']}: {s['cpu_usage']}%")

regions = {}
for server in servers:
    region = server["region"]
    regions.setdefault(region, [])
    regions[region].append(server["name"])
print("\n  Servers by region:")
for region, names in regions.items():
    print(f"    {region}: {', '.join(names)}")

print("\n=== Writing with DictWriter ===")
report_path = Path("fundamentals/file_handling/server_report.csv")
with open(report_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "status", "cpu_usage", "alert"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for server in servers:
        alert = "HIGH CPU" if server["cpu_usage"] > 80 else "OK"
        writer.writerow({
            "name":      server["name"],
            "status":    server["status"],
            "cpu_usage": server["cpu_usage"],
            "alert":     alert,
        })
print(f"  Report written: {report_path}")
print("\ncsv_processing.py executed successfully.")