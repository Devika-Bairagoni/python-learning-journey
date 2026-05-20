"""
while_loop_patterns.py

Demonstrates while loops for retry logic, polling, and condition-based iteration.
These patterns appear directly in backend services and API clients.

Author: [Your Name]
"""

# --- Pattern 1: Retry with backoff simulation ---
# This is real. Every HTTP client, database connector, and cloud SDK has
# retry logic that looks exactly like this.

MAX_RETRIES = 3
attempt = 0
success = False

print("=== Connection Retry Simulation ===")
while attempt < MAX_RETRIES and not success:
    attempt += 1  # increment first — prevents forgetting and causing infinite loops
    print(f"  Attempt {attempt}/{MAX_RETRIES}: connecting to database...")

    # Simulate: third attempt succeeds
    if attempt == 3:
        success = True
        print(f"  Connection established on attempt {attempt}.")

if not success:
    print("  All retries exhausted. Raising connection error.")


# --- Pattern 2: Processing a queue until empty ---
# In backend systems: message queues, task queues, job queues
task_queue = ["send_email", "generate_report", "backup_db"]

print("\n=== Task Queue Processor ===")
while task_queue:
    # `while task_queue` is True as long as the list is non-empty
    # This is Pythonic — don't write `while len(task_queue) > 0`
    current_task = task_queue.pop(0)  # remove and return first item
    print(f"  Processing: {current_task}")

print("  Queue empty. All tasks complete.")