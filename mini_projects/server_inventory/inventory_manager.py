"""
inventory_manager.py

Manages a server infrastructure inventory loaded from JSON.
Demonstrates real-world dict usage: loading JSON, filtering,
grouping, aggregating, and generating reports.

Real-world relevance:
  - Cloud providers (AWS, GCP, Azure) expose infrastructure
    exactly like this through their APIs
  - Infrastructure-as-Code tools (Terraform, Ansible) use
    this exact data shape
  - This is your first taste of working with JSON APIs

Usage:
    python mini_projects/server_inventory/inventory_manager.py

Author: [Your Name]
Date: [Today's Date]
"""

import json   # built-in Python module — no installation needed


def load_inventory(filepath: str) -> list:
    """
    Load server inventory from a JSON file.
    Returns list of server dictionaries.
    """
    try:
        with open(filepath, "r") as file:
            data = json.load(file)       # parse JSON into Python dict
            return data.get("servers", [])
    except FileNotFoundError:
        print(f"ERROR: Inventory file not found — {filepath}")
        return []
    except json.JSONDecodeError:
        print(f"ERROR: Invalid JSON in file — {filepath}")
        return []


def group_by_region(servers: list) -> dict:
    """
    Group servers by region.
    Returns dict mapping region name to list of servers.

    Example output:
        {"us-east-1": [...], "us-west-2": [...]}
    """
    grouped = {}
    for server in servers:
        region = server["region"]
        grouped.setdefault(region, [])
        grouped[region].append(server)
    return grouped


def group_by_status(servers: list) -> dict:
    """Group servers by their current status."""
    grouped = {}
    for server in servers:
        status = server["status"]
        grouped.setdefault(status, [])
        grouped[status].append(server)
    return grouped


def get_high_cpu_servers(servers: list, threshold: float = 80.0) -> list:
    """Return servers with CPU usage above threshold."""
    return [s for s in servers if s["cpu_usage"] > threshold]


def get_total_resources(servers: list) -> dict:
    """
    Calculate total CPU, memory, and storage across all servers.
    Returns summary dict.
    """
    return {
        "total_cpu_cores": sum(s["specs"]["cpu_cores"] for s in servers),
        "total_memory_gb": sum(s["specs"]["memory_gb"] for s in servers),
        "total_storage_gb": sum(s["specs"]["storage_gb"] for s in servers),
    }


def generate_report(servers: list) -> None:
    """Print a full infrastructure inventory report."""
    if not servers:
        print("No servers in inventory.")
        return

    by_status = group_by_status(servers)
    by_region = group_by_region(servers)
    high_cpu  = get_high_cpu_servers(servers)
    resources = get_total_resources(servers)

    # --- Header ---
    print("=" * 58)
    print("       SERVER INVENTORY REPORT")
    print("=" * 58)
    print(f"  Total servers     : {len(servers)}")
    print(f"  Running           : {len(by_status.get('running', []))}")
    print(f"  Degraded          : {len(by_status.get('degraded', []))}")
    print(f"  Stopped           : {len(by_status.get('stopped', []))}")
    print(f"  Regions active    : {len(by_region)}")

    # --- Total resources ---
    print("\n  TOTAL RESOURCES:")
    print(f"    CPU cores  : {resources['total_cpu_cores']}")
    print(f"    Memory     : {resources['total_memory_gb']} GB")
    print(f"    Storage    : {resources['total_storage_gb']} GB")

    # --- Full server list ---
    print("\n  FULL INVENTORY:")
    print(f"  {'ID':<10} {'Name':<20} {'Region':<12} {'Status':<10} {'CPU%':>5}")
    print("  " + "-" * 54)

    for server in servers:
        # Flag high CPU visually
        cpu_flag = " ⚠" if server["cpu_usage"] > 80 else ""
        print(
            f"  {server['id']:<10} "
            f"{server['name']:<20} "
            f"{server['region']:<12} "
            f"{server['status']:<10} "
            f"{server['cpu_usage']:>5.1f}%"
            f"{cpu_flag}"
        )

    # --- Regional breakdown ---
    print("\n  BY REGION:")
    for region, region_servers in by_region.items():
        names = [s["name"] for s in region_servers]
        print(f"    {region}: {', '.join(names)}")

    # --- Alerts ---
    if high_cpu:
        print(f"\n  ⚠ HIGH CPU ALERT (> 80%):")
        for server in high_cpu:
            print(f"    • {server['name']} — {server['cpu_usage']}% CPU")

    if "degraded" in by_status:
        print(f"\n  ⚠ DEGRADED SERVERS:")
        for server in by_status["degraded"]:
            print(f"    • {server['name']} in {server['region']}")

    print("=" * 58)


if __name__ == "__main__":
    FILE_PATH = "mini_projects/server_inventory/inventory.json"

    print(f"Loading inventory from: {FILE_PATH}\n")
    servers = load_inventory(FILE_PATH)
    generate_report(servers)