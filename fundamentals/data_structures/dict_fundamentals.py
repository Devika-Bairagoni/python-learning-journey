"""
dict_fundamentals.py

Core dictionary concepts: creation, access, update, deletion.
Dictionaries are the foundation of JSON, APIs, configs, and databases.

Author: [Your Name]
"""

# --- Creating dictionaries ---
# A dict maps keys to values. Keys must be unique and immutable (strings, numbers).
# Values can be anything.

server = {
    "name": "api-server-01",
    "ip": "192.168.1.10",
    "port": 8000,
    "active": True,
    "cpu_usage": 45.2,
}

# --- Accessing values ---
# Use the key inside square brackets — like an index, but named.

print("=== Accessing Values ===")
print(server["name"])      # "api-server-01"
print(server["port"])      # 8000


# --- Safe access with .get() ---
# CRITICAL HABIT: always use .get() when the key might not exist.
# Using server["missing_key"] CRASHES with KeyError.
# server.get("missing_key") returns None safely.

print("\n=== Safe Access ===")
print(server.get("ip"))              # "192.168.1.10"
print(server.get("region"))          # None — key doesn't exist, no crash
print(server.get("region", "us-east-1"))  # "us-east-1" — default value


# --- Updating values ---
print("\n=== Updating ===")
server["cpu_usage"] = 67.8           # update existing key
server["memory_gb"] = 16             # add new key
print(server)


# --- Deleting keys ---
print("\n=== Deleting ===")
del server["memory_gb"]              # delete by key
popped = server.pop("cpu_usage")     # remove and return value
print(f"Removed cpu_usage: {popped}")
print(server)


# --- Checking key existence ---
print("\n=== Membership ===")
print("name" in server)          # True
print("region" in server)        # False

# Production pattern: check before accessing
if "active" in server:
    status = "online" if server["active"] else "offline"
    print(f"Server status: {status}")


# --- Dictionary length ---
print(f"\nTotal fields tracked: {len(server)}")