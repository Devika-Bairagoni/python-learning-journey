"""
nested_structures.py

Nested dicts and mixed structures: dicts inside lists, lists inside dicts.
This is the exact shape of every JSON API response you will ever work with.

Author: [Your Name]
"""

# --- Nested dictionary ---
# A dict whose values are themselves dicts.
# This is how config files, user profiles, and API responses are structured.

infrastructure = {
    "production": {
        "api_server": {
            "host": "api.myapp.com",
            "port": 443,
            "ssl": True,
            "replicas": 3,
        },
        "database": {
            "host": "db.myapp.com",
            "port": 5432,
            "name": "prod_db",
        },
    },
    "staging": {
        "api_server": {
            "host": "staging-api.myapp.com",
            "port": 8080,
            "ssl": False,
            "replicas": 1,
        },
        "database": {
            "host": "staging-db.myapp.com",
            "port": 5432,
            "name": "staging_db",
        },
    },
}

# --- Accessing nested values ---
# Chain square brackets or .get() for each level

print("=== Accessing Nested Values ===")
prod_port = infrastructure["production"]["api_server"]["port"]
print(f"Production API port: {prod_port}")

# Safe nested access — chain .get() to avoid KeyError at any level
staging_ssl = (
    infrastructure
    .get("staging", {})
    .get("api_server", {})
    .get("ssl", False)
)
print(f"Staging SSL enabled: {staging_ssl}")


# --- List of dicts — the most common API response shape ---
# When you call GET /api/users, you get back something like this:

api_response = {
    "status": "success",
    "total": 3,
    "data": [
        {"id": 1, "name": "Alice", "role": "admin",  "active": True},
        {"id": 2, "name": "Bob",   "role": "viewer", "active": False},
        {"id": 3, "name": "Carol", "role": "editor", "active": True},
    ]
}

# --- Processing the response like a backend engineer ---
print("\n=== Processing API Response ===")
print(f"Status : {api_response['status']}")
print(f"Total  : {api_response['total']}")

# Iterate over the data list
active_users = [
    user for user in api_response["data"]
    if user["active"]
]

print(f"Active users ({len(active_users)}):")
for user in active_users:
    print(f"  [{user['id']}] {user['name']} — {user['role']}")


# --- Modifying nested structures ---
print("\n=== Updating Nested Values ===")
infrastructure["production"]["api_server"]["replicas"] = 5
print(f"Updated replicas: {infrastructure['production']['api_server']['replicas']}")

# Add a new environment
infrastructure["development"] = {
    "api_server": {"host": "localhost", "port": 8000, "ssl": False, "replicas": 1},
    "database":   {"host": "localhost", "port": 5432, "name": "dev_db"},
}
print(f"Environments: {list(infrastructure.keys())}")