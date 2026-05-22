"""
list_operations.py

Sorting, searching, aggregating, and combining lists.
These are the operations behind every data API and reporting system.

Author: [Your Name]
"""

# --- Sorting ---
# sorted() returns a NEW list — original unchanged
# list.sort() modifies IN PLACE — original changed

response_times = [340, 89, 210, 456, 78, 120]

print("=== Sorting ===")
ascending = sorted(response_times)           # new list, original untouched
descending = sorted(response_times, reverse=True)

print(f"Original : {response_times}")
print(f"Ascending: {ascending}")
print(f"Descending: {descending}")

# Sorting objects by a key — this is how you sort API results
servers = [
    {"name": "api-01", "load": 78},
    {"name": "db-01",  "load": 92},
    {"name": "api-02", "load": 34},
]

# sorted by load — lambda defines WHAT to sort by
by_load = sorted(servers, key=lambda s: s["load"])
print("\nServers by load (low to high):")
for server in by_load:
    print(f"  {server['name']}: {server['load']}%")


# --- Aggregation ---
print("\n=== Aggregation ===")
scores = [88, 92, 75, 61, 99, 83, 70]

print(f"Highest : {max(scores)}")
print(f"Lowest  : {min(scores)}")
print(f"Total   : {sum(scores)}")
print(f"Average : {sum(scores) / len(scores):.2f}")   # :.2f = 2 decimal places


# --- Filtering with a loop (traditional) ---
# We will improve this with comprehensions in the next file

print("\n=== Filtering ===")
failing_scores = []
for score in scores:
    if score < 70:
        failing_scores.append(score)

print(f"Failing scores (< 70): {failing_scores}")


# --- Combining lists ---
print("\n=== Combining ===")
team_a = ["Alice", "Bob"]
team_b = ["Charlie", "Diana"]

full_team = team_a + team_b        # concatenation — creates new list
print(f"Full team: {full_team}")

team_a.extend(team_b)              # extend — adds all items from team_b INTO team_a
print(f"After extend: {team_a}")   # team_a is now modified


# --- Counting and finding ---
print("\n=== Counting ===")
log_levels = ["INFO", "ERROR", "INFO", "WARNING", "ERROR", "INFO"]

print(f"ERROR count : {log_levels.count('ERROR')}")
print(f"INFO count  : {log_levels.count('INFO')}")
print(f"First ERROR at index: {log_levels.index('ERROR')}")