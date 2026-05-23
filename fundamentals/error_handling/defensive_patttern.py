"""
defensive_patterns.py

Production-grade defensive patterns:
- Input validation before processing
- Fail fast vs fail safe decisions
- Logging errors instead of silently swallowing them
- Re-raising exceptions when appropriate

Author: [Your Name]
"""


# --- Anti-pattern 1: Catching everything silently ---
# This is the most dangerous mistake in exception handling.
# It hides bugs and makes debugging impossible.

print("=== Anti-patterns to Avoid ===")

def bad_divide(a, b):
    try:
        return a / b
    except:
        pass   # NEVER do this — swallows ALL errors silently
               # If something breaks, you will never know why

# This hides a real bug — b is a string, not a number
result = bad_divide(10, "five")
print(f"  bad_divide result: {result}")   # None — no error, no clue why


# --- Pattern 1: Validate inputs before processing (fail fast) ---
# Catch problems at the entry point, not deep inside your logic.

print("\n=== Fail Fast Validation ===")

def calculate_average(scores: list) -> float:
    """Calculate average with input validation at the start."""

    if not isinstance(scores, list):
        raise TypeError(f"Expected list, got {type(scores).__name__}")

    if len(scores) == 0:
        raise ValueError("Cannot calculate average of empty list")

    if not all(isinstance(s, (int, float)) for s in scores):
        raise ValueError("All scores must be numeric")

    return sum(scores) / len(scores)


test_cases = [
    [88, 92, 75],      # valid
    [],                 # empty list
    "not a list",       # wrong type
    [88, "A", 75],      # mixed types
]

for case in test_cases:
    try:
        avg = calculate_average(case)
        print(f"  Average of {case}: {avg:.2f}")
    except (TypeError, ValueError) as e:
        print(f"  Validation error: {e}")


# --- Pattern 2: Re-raising with context ---
# Sometimes you catch an exception to add context, then re-raise it.
# This gives the caller better information without losing the original error.

print("\n=== Re-raising with Context ===")

def load_user_scores(filepath: str) -> list:
    """Load scores from file, adding context to any errors."""
    try:
        with open(filepath, "r") as f:
            content = f.read()
            scores = [int(x.strip()) for x in content.split(",")]
            return scores
    except FileNotFoundError as e:
        # Re-raise with added context — 'from e' preserves the original error
        raise FileNotFoundError(
            f"Score file missing — check path: {filepath}"
        ) from e
    except ValueError as e:
        raise ValueError(
            f"Score file contains non-numeric data: {filepath}"
        ) from e


try:
    scores = load_user_scores("missing_scores.txt")
except FileNotFoundError as e:
    print(f"  Error: {e}")


# --- Pattern 3: Context managers (with statement) ---
# The 'with' statement handles cleanup automatically.
# No need for try/finally to close files — 'with' does it for you.

print("\n=== Context Manager Pattern ===")

# Without context manager — fragile
try:
    f = open("fundamentals/error_handling/exception_basics.py", "r")
    content = f.read(50)
    f.close()   # what if an exception happens before this? file stays open!
except FileNotFoundError:
    pass

# With context manager — file ALWAYS closes, even if exception occurs
try:
    with open("fundamentals/error_handling/exception_basics.py", "r") as f:
        content = f.read(50)
        print(f"  Read: {content[:30]}...")
    # file is automatically closed here — no explicit f.close() needed
except FileNotFoundError as e:
    print(f"  File error: {e}")