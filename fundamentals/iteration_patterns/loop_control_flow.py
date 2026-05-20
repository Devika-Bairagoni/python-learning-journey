"""
loop_control_flow.py

break, continue, and the loop else clause.
These are control signals — they change what a loop does mid-execution.

Author: [Your Name]
"""

# --- break: exit the loop immediately ---
# Use case: found what you were searching for, no need to keep looping

log_entries = [
    "INFO: server started",
    "INFO: connection accepted",
    "ERROR: disk space critical",  # ← stop here and alert
    "INFO: request processed",
]

print("=== Scanning logs for first critical error ===")
for entry in log_entries:
    if entry.startswith("ERROR"):
        print(f"  CRITICAL found: {entry}")
        break  # stop scanning — we found the problem
    print(f"  OK: {entry}")


# --- continue: skip this iteration, move to next ---
# Use case: filter out items you don't want to process

print("\n=== Processing only ERROR entries ===")
for entry in log_entries:
    if not entry.startswith("ERROR"):
        continue  # skip INFO entries — we only care about errors
    print(f"  Processing error: {entry}")


# --- for/else: runs if loop completed WITHOUT break ---
# This pattern is almost unknown to beginners but used in real search logic.
# If the loop finishes without a break, the else block runs.

search_term = "CRITICAL"

print(f"\n=== Searching for '{search_term}' ===")
for entry in log_entries:
    if search_term in entry:
        print(f"  Found: {entry}")
        break
else:
    # This only runs if no `break` occurred
    print(f"  '{search_term}' not found in logs.")