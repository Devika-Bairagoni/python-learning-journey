"""
dict_comprehensions.py

Dict comprehensions: build dictionaries from any iterable in one line.
Same concept as list comprehensions — different output shape.

Syntax: {key_expr: value_expr for item in iterable if condition}

Author: [Your Name]
"""

# --- Basic dict comprehension ---
# Build a lookup table: server name → port number

server_names = ["api-01", "api-02", "db-01", "cache-01"]
ports = [8001, 8002, 5432, 6379]

# Traditional way
port_map = {}
for name, port in zip(server_names, ports):
    port_map[name] = port

# Comprehension way — same result
port_map = {name: port for name, port in zip(server_names, ports)}
print(f"Port map: {port_map}")

# Look up instantly by name — O(1) speed
print(f"db-01 port: {port_map['db-01']}")


# --- Transforming an existing dict ---
scores = {"Alice": 88, "Bob": 61, "Charlie": 95, "Diana": 72}

# Convert all scores to letter grades
def get_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

grade_map = {name: get_grade(score) for name, score in scores.items()}
print(f"\nGrade map: {grade_map}")


# --- Filtering a dict ---
# Keep only students who are passing

passing = {name: score for name, score in scores.items() if score >= 70}
print(f"Passing students: {passing}")


# --- Inverting a dict (swap keys and values) ---
# Production use: reverse lookup tables

original = {"api-01": 8001, "db-01": 5432, "cache-01": 6379}
inverted = {port: name for name, port in original.items()}
print(f"\nPort to server lookup: {inverted}")
print(f"Who is on port 5432? {inverted[5432]}")


# --- Real-world pattern: indexing a list of dicts by a key ---
# This is how you turn a database result list into a fast-lookup dict

users = [
    {"id": 1, "name": "Alice", "role": "admin"},
    {"id": 2, "name": "Bob",   "role": "viewer"},
    {"id": 3, "name": "Carol", "role": "editor"},
]

# Build a lookup dict: id → user record
# In production: you do this ONCE after a DB query,
# then look up by ID in O(1) instead of searching the list every time
user_by_id = {user["id"]: user for user in users}

print(f"\nUser 2: {user_by_id[2]}")
print(f"User 3 role: {user_by_id[3]['role']}")