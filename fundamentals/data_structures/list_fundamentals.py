"""
list_fundamentals.py

Core list concepts: creation, indexing, slicing, mutation.
Every backend engineer uses these patterns daily.

Author: [Your Name]
"""

# --- Creating lists ---
# Lists hold ordered collections of items.
# Items can be any type — strings, numbers, even other lists.

servers = ["api-01", "api-02", "db-01", "cache-01"]
response_times = [120, 340, 89, 210, 456, 78]
mixed = ["error", 404, True, 3.14]  # valid but avoid in production — keep types consistent


# --- Indexing — accessing single items ---
# Python uses zero-based indexing. First item is index 0.

print("=== Indexing ===")
print(servers[0])    # "api-01"  — first item
print(servers[-1])   # "cache-01" — last item (negative index counts from end)
print(servers[-2])   # "db-01"   — second from last


# --- Slicing — accessing a range of items ---
# Syntax: list[start:stop:step]
# start is INCLUSIVE, stop is EXCLUSIVE

print("\n=== Slicing ===")
print(response_times[0:3])    # [120, 340, 89]  — first 3 items
print(response_times[2:])     # from index 2 to end
print(response_times[:3])     # from start to index 3 (exclusive)
print(response_times[::2])    # every second item — step of 2
print(response_times[::-1])   # reversed list — very common pattern


# --- Mutation — lists are mutable (changeable) ---
# This is different from strings, which are immutable.

print("\n=== Mutation ===")
servers[1] = "api-02-upgraded"   # replace item at index 1
print(servers)

servers.append("backup-01")      # add to end
print(servers)

servers.insert(0, "load-balancer")  # insert at specific position
print(servers)

removed = servers.pop()          # remove and return last item
print(f"Removed: {removed}")
print(servers)

servers.remove("api-02-upgraded")  # remove by value (first match)
print(servers)


# --- Checking membership ---
print("\n=== Membership ===")
print("db-01" in servers)         # True
print("ghost-server" in servers)  # False

# This is how you guard against KeyErrors and missing data in production
target = "db-01"
if target in servers:
    print(f"  {target} is active")
else:
    print(f"  {target} not found — check configuration")


# --- Length ---
print(f"\nTotal servers tracked: {len(servers)}")