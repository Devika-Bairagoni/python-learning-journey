"""
dict_operations.py

Iterating, merging, and working with dict views.
These patterns appear in every config system, API handler, and data pipeline.

Author: [Your Name]
"""

config = {
    "host": "localhost",
    "port": 5432,
    "database": "prod_db",
    "user": "admin",
    "timeout": 30,
}


# --- Iterating dictionaries ---
# Three ways — each serves a different purpose in production

print("=== Keys only ===")
for key in config.keys():
    print(f"  {key}")

print("\n=== Values only ===")
for value in config.values():
    print(f"  {value}")

print("\n=== Keys AND values — use this most often ===")
for key, value in config.items():
    # .items() returns (key, value) pairs — this is the professional way
    print(f"  {key}: {value}")


# --- Merging dictionaries ---
# In production: merging default config with user-provided overrides

defaults = {
    "timeout": 30,
    "max_retries": 3,
    "ssl": False,
    "port": 5432,
}

overrides = {
    "ssl": True,          # user wants SSL enabled
    "timeout": 60,        # user wants longer timeout
}

# Python 3.9+ merge operator — clean and readable
merged = defaults | overrides
print(f"\n=== Merged Config ===")
for key, value in merged.items():
    print(f"  {key}: {value}")

# Older Python way (still valid, widely used)
merged_old = {**defaults, **overrides}   # ** unpacks dict into key=value pairs


# --- Building dicts dynamically ---
# This pattern is everywhere: constructing API request bodies,
# building database records, assembling config objects

print("\n=== Building Dynamically ===")
fields = ["name", "email", "role"]
values = ["Alice", "alice@company.com", "engineer"]

# zip pairs the two lists, dict() converts to dictionary
user_record = dict(zip(fields, values))
print(f"User record: {user_record}")


# --- setdefault() — only set if key doesn't exist ---
# Production use: initializing counters, building grouped data

print("\n=== setdefault ===")
log_counts = {}
log_levels = ["INFO", "ERROR", "INFO", "WARNING", "ERROR", "INFO"]

for level in log_levels:
    # If key doesn't exist, set it to 0. Then increment.
    log_counts.setdefault(level, 0)
    log_counts[level] += 1

print(f"Log counts: {log_counts}")