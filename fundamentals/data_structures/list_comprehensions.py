"""
list_comprehensions.py

List comprehensions: the most important Pythonic skill for data processing.
Used in every AI pipeline, data API, and backend service.

Syntax: [expression for item in iterable if condition]

Author: [Your Name]
"""

# --- The problem with traditional loops ---
# This works, but it is verbose for simple transformations

scores = [88, 92, 75, 61, 99, 83, 70, 45]

# Traditional way
passing_scores = []
for score in scores:
    if score >= 70:
        passing_scores.append(score)


# --- Comprehension way ---
# Same logic, one line, more readable once you know the pattern

passing_scores = [score for score in scores if score >= 70]
print(f"Passing scores: {passing_scores}")


# --- Transformation comprehensions ---
# Not just filtering — also transforming each item

print("\n=== Transformations ===")

# Convert all names to uppercase
names = ["alice", "bob", "charlie", "diana"]
upper_names = [name.upper() for name in names]
print(f"Uppercase: {upper_names}")

# Calculate letter grades from numeric scores
def get_grade(score: int) -> str:
    """Convert numeric score to letter grade."""
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

letter_grades = [get_grade(score) for score in scores]
print(f"Letter grades: {letter_grades}")


# --- Filter + transform together ---
# Get letter grades for ONLY failing students

failing_grades = [
    f"Score {score} -> {get_grade(score)}"
    for score in scores
    if score < 70
]
print(f"\nFailing students: {failing_grades}")


# --- Real-world pattern: extracting a field from a list of dicts ---
# This is what you do every time you process API responses or DB rows

users = [
    {"id": 1, "name": "Alice", "active": True},
    {"id": 2, "name": "Bob",   "active": False},
    {"id": 3, "name": "Carol", "active": True},
]

# Extract just the names of active users
active_names = [user["name"] for user in users if user["active"]]
print(f"\nActive users: {active_names}")

# Extract all IDs
all_ids = [user["id"] for user in users]
print(f"All user IDs: {all_ids}")


# --- When NOT to use comprehensions ---
# Rule: if the logic inside is more than one condition or one function call,
# use a regular loop. Comprehensions are for SIMPLE transformations.

# Too complex for a comprehension — use a regular loop instead
results = []
for user in users:
    if user["active"]:
        name = user["name"].upper()
        label = f"[ACTIVE] {name} (ID: {user['id']})"
        results.append(label)
print(f"\nFormatted: {results}")