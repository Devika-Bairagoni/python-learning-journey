"""
log_analyzer.py

Analyzes server log files and generates a structured summary report.

Purpose: Demonstrates real-world loop usage — reading files, filtering data,
         counting occurrences, and formatting output for human readers.

This pattern appears in:
  - Production monitoring systems
  - CI/CD pipeline log parsers
  - Cloud log aggregation services (CloudWatch, Datadog, Loki)

Usage:
    python log_analyzer.py

Author: [Your Name]
Date: [Today's Date]
"""


def load_logs(filepath: str) -> list:
    """
    Read log file and return list of log entry strings.

    In production this would read from cloud storage or a logging API.
    For now, we read from a local file.
    """
    try:
        with open(filepath, "r") as file:
            # strip() removes trailing newline from each line
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: Log file not found at {filepath}")
        return []


def count_log_levels(log_entries: list) -> dict:
    """
    Count occurrences of each log level (INFO, WARNING, ERROR, DEBUG).

    Returns a dictionary mapping log level to count.
    Example: {"INFO": 12, "ERROR": 3, "WARNING": 2}
    """
    counts = {
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "DEBUG": 0,
        "UNKNOWN": 0,
    }

    for entry in log_entries:
        # Entry format: "LEVEL: message"
        # We check which level prefix the entry starts with
        classified = False
        for level in ["INFO", "WARNING", "ERROR", "DEBUG"]:
            if entry.startswith(level):
                counts[level] += 1
                classified = True
                break  # once we find the level, stop checking others

        if not classified:
            counts["UNKNOWN"] += 1

    return counts


def extract_errors(log_entries: list) -> list:
    """
    Return only ERROR-level log entries.

    In production: these would be sent to an alerting system (PagerDuty, Slack).
    """
    errors = []

    for entry in log_entries:
        if entry.startswith("ERROR"):
            errors.append(entry)

    return errors


def generate_report(log_entries: list) -> None:
    """
    Print a structured summary report to the console.

    In production: this output would be written to a file,
    sent to a dashboard, or posted to a Slack channel.
    """
    if not log_entries:
        print("No log entries to analyze.")
        return

    counts = count_log_levels(log_entries)
    errors = extract_errors(log_entries)
    total = len(log_entries)

    print("=" * 50)
    print("  LOG ANALYSIS REPORT")
    print("=" * 50)
    print(f"  Total entries analyzed : {total}")
    print()

    print("  Log Level Breakdown:")
    for level, count in counts.items():
        # Skip levels with zero entries — clean output
        if count == 0:
            continue
        percentage = (count / total) * 100
        bar = "█" * int(percentage / 5)  # simple ASCII bar chart
        print(f"    {level:<10} {count:>4}  {bar} {percentage:.1f}%")

    print()
    if errors:
        print(f"  ERROR Details ({len(errors)} found):")
        for index, error in enumerate(errors, start=1):
            print(f"    [{index}] {error}")
    else:
        print("  No errors found. System healthy.")

    print("=" * 50)


# --- Entry point ---
# In Python, this block only runs when you execute this file directly.
# It does NOT run when another file imports this module.
# This is standard Python architecture — always structure your files this way.

if __name__ == "__main__":
    LOG_FILE_PATH = "mini_projects/log_analyzer/sample_logs.txt"

    print(f"Loading logs from: {LOG_FILE_PATH}\n")
    entries = load_logs(LOG_FILE_PATH)
    generate_report(entries)