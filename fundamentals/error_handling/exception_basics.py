"""
exception_basics.py

Core exception handling: try/except/else/finally.
Understanding what each block does and when it runs.

Author: [Your Name]
"""

# --- The most common exceptions you will encounter ---
# Knowing their names lets you catch them specifically.

# FileNotFoundError  — file doesn't exist
# KeyError           — dict key doesn't exist
# IndexError         — list index out of range
# ValueError         — wrong value type or format
# TypeError          — wrong data type passed
# ZeroDivisionError  — dividing by zero
# AttributeError     — calling method that doesn't exist
# json.JSONDecodeError — malformed JSON


# --- Basic try/except ---
print("=== Basic try/except ===")

# Without handling — this crashes entire program
# print(10 / 0)   # ZeroDivisionError

# With handling — program continues
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  Cannot divide by zero — using default value")
    result = 0

print(f"  Result: {result}")


# --- Catching multiple specific exceptions ---
print("\n=== Multiple Exceptions ===")

def parse_user_age(value: str) -> int:
    """
    Parse age from string input.
    Handles both non-numeric input and negative age.
    """
    try:
        age = int(value)           # may raise ValueError if not a number

        if age < 0 or age > 150:
            raise ValueError(f"Age {age} is outside realistic range")

        return age

    except ValueError as e:
        # 'as e' captures the exception object — gives you the message
        print(f"  Invalid age input: {e}")
        return None

print(f"  Valid input: {parse_user_age('25')}")
print(f"  String input: {parse_user_age('twenty')}")
print(f"  Negative age: {parse_user_age('-5')}")
print(f"  Too old: {parse_user_age('200')}")


# --- try / except / else / finally ---
print("\n=== Full Structure ===")

def read_first_line(filepath: str) -> str:
    """
    Demonstrates all four exception blocks.
    - try: attempt the operation
    - except: handle failure
    - else: runs only on success (no exception)
    - finally: ALWAYS runs — use for cleanup
    """
    file = None
    try:
        file = open(filepath, "r")
        first_line = file.readline().strip()

    except FileNotFoundError:
        print(f"  File not found: {filepath}")
        return None

    except PermissionError:
        print(f"  Permission denied: {filepath}")
        return None

    else:
        # Only runs if try block succeeded with no exception
        print(f"  Successfully read file: {filepath}")
        return first_line

    finally:
        # ALWAYS runs — whether exception occurred or not
        # Use for cleanup: closing files, releasing locks, closing DB connections
        if file:
            file.close()
            print("  File handle closed.")


result = read_first_line("fundamentals/error_handling/exception_basics.py")
print(f"  First line: {result}")

result = read_first_line("nonexistent_file.txt")
print(f"  Result: {result}")