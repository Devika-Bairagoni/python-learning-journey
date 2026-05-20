"""
for_loop_patterns.py

Demonstrates professional iteration patterns using for loops.
Focus: real-world data processing, not toy examples.

Author: [Your Name]
"""

# --- Pattern 1: Basic iteration over a collection ---
# In production, this collection would come from a database query or API response.
server_names = ["api-server-01", "api-server-02", "db-server-01"]

print("=== Active Servers ===")
for server in server_names:
    # 'server' is our loop variable — name it after what it represents
    print(f"  Checking: {server}")


# --- Pattern 2: enumerate() — always use this when you need an index ---
# This is how you'd number items in a report, build a numbered menu,
# or track position in a pipeline.

print("\n=== Server Health Report ===")
for position, server in enumerate(server_names, start=1):
    # start=1 makes it human-readable (1, 2, 3) instead of (0, 1, 2)
    print(f"  [{position}] {server}: OK")


# --- Pattern 3: zip() — iterate two collections in parallel ---
# In production: pairing request IDs with response codes,
# names with email addresses, etc.

servers = ["api-server-01", "db-server-01", "cache-01"]
statuses = ["healthy", "degraded", "healthy"]

print("\n=== Server Status Summary ===")
for server, status in zip(servers, statuses):
    # zip() pairs items by position — stops at the shorter list
    print(f"  {server}: {status}")


# --- Pattern 4: range() — when you need a numeric sequence ---
# Use this for batch processing, pagination, retry logic
TOTAL_PAGES = 5

print("\n=== Simulating Paginated API Fetch ===")
for page in range(1, TOTAL_PAGES + 1):
    # range(1, 6) gives 1,2,3,4,5 — never hardcode the end value
    # TOTAL_PAGES is a named constant (uppercase = convention for constants)
    print(f"  Fetching page {page} of {TOTAL_PAGES}...")