from pathlib import Path

files = {}

files["fundamentals/file_handling/file_basics.py"] = """
from pathlib import Path

output_path = Path("fundamentals/file_handling/sample_output.txt")

print("=== Writing a file ===")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("Line 1: Server started\\n")
    f.write("Line 2: Database connected\\n")
    f.write("Line 3: Listening on port 8000\\n")
print(f"  Written to: {output_path}")

print("\\n=== Reading entire file ===")
with open(output_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

print("=== Reading line by line ===")
with open(output_path, "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        print(f"  [{line_number}] {line.strip()}")

print("\\n=== Appending to file ===")
with open(output_path, "a", encoding="utf-8") as f:
    f.write("Line 4: New connection accepted\\n")
    f.write("Line 5: Request processed\\n")
with open(output_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"  File now has {len(lines)} lines")

print("\\n=== Safe file access ===")
missing_path = Path("does_not_exist.txt")
if missing_path.exists():
    with open(missing_path, "r", encoding="utf-8") as f:
        print(f.read())
else:
    print(f"  File not found: {missing_path}")
    print("  Skipping read operation safely.")

print("\\nfile_basics.py executed successfully.")
""".strip()

files["fundamentals/file_handling/pathlib_patterns.py"] = """
from pathlib import Path

print("=== Creating Paths ===")
project_root = Path(".")
logs_dir = project_root / "fundamentals" / "file_handling"
output_file = logs_dir / "pathlib_output.txt"
print(f"  Project root : {project_root.resolve()}")
print(f"  Logs dir     : {logs_dir}")
print(f"  Output file  : {output_file}")

print("\\n=== Path Properties ===")
sample = Path("mini_projects/config_loader/config_valid.json")
print(f"  Name     : {sample.name}")
print(f"  Stem     : {sample.stem}")
print(f"  Suffix   : {sample.suffix}")
print(f"  Parent   : {sample.parent}")
print(f"  Exists   : {sample.exists()}")

print("\\n=== Creating Directories ===")
new_dir = Path("fundamentals/file_handling/test_output")
new_dir.mkdir(parents=True, exist_ok=True)
print(f"  Created: {new_dir}")

print("\\n=== pathlib Read/Write ===")
test_file = new_dir / "test.txt"
test_file.write_text("Hello from pathlib!\\nLine 2\\nLine 3", encoding="utf-8")
content = test_file.read_text(encoding="utf-8")
print(f"  Content:\\n{content}")

print("\\n=== Listing Python Files ===")
project = Path("fundamentals")
python_files = list(project.glob("**/*.py"))
print(f"  Python files found: {len(python_files)}")
for py_file in python_files[:5]:
    print(f"    {py_file}")

print("\\n=== File Metadata ===")
config_file = Path("mini_projects/config_loader/config_valid.json")
if config_file.exists():
    stat = config_file.stat()
    size_kb = stat.st_size / 1024
    print(f"  File      : {config_file.name}")
    print(f"  Size      : {size_kb:.2f} KB")
    print(f"  Is file   : {config_file.is_file()}")
    print(f"  Is folder : {config_file.is_dir()}")

print("\\npathlib_patterns.py executed successfully.")
""".strip()

files["fundamentals/file_handling/csv_processing.py"] = """
import csv
from pathlib import Path

print("=== Writing CSV ===")
output_path = Path("fundamentals/file_handling/servers.csv")
headers = ["server_id", "name", "region", "status", "cpu_usage"]
rows = [
    ["srv-001", "api-server-01", "us-east-1", "running",  45.2],
    ["srv-002", "db-server-01",  "us-east-1", "running",  78.9],
    ["srv-003", "cache-01",      "us-west-2", "degraded", 91.3],
    ["srv-004", "api-server-02", "us-west-2", "stopped",   0.0],
]
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)
print(f"  Written: {output_path}")

print("\\n=== Reading CSV ===")
with open(output_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    servers = [row for row in reader]
print(f"  Loaded {len(servers)} servers")
for server in servers:
    print(f"  {server['server_id']} | {server['name']} | {server['status']}")

print("\\n=== Processing CSV Data ===")
for server in servers:
    server["cpu_usage"] = float(server["cpu_usage"])
high_cpu = [s for s in servers if s["cpu_usage"] > 80]
print(f"  High CPU servers: {len(high_cpu)}")
for s in high_cpu:
    print(f"    {s['name']}: {s['cpu_usage']}%")

regions = {}
for server in servers:
    region = server["region"]
    regions.setdefault(region, [])
    regions[region].append(server["name"])
print("\\n  Servers by region:")
for region, names in regions.items():
    print(f"    {region}: {', '.join(names)}")

print("\\n=== Writing with DictWriter ===")
report_path = Path("fundamentals/file_handling/server_report.csv")
with open(report_path, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["name", "status", "cpu_usage", "alert"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for server in servers:
        alert = "HIGH CPU" if server["cpu_usage"] > 80 else "OK"
        writer.writerow({
            "name":      server["name"],
            "status":    server["status"],
            "cpu_usage": server["cpu_usage"],
            "alert":     alert,
        })
print(f"  Report written: {report_path}")
print("\\ncsv_processing.py executed successfully.")
""".strip()

files["mini_projects/activity_logger/sample_activities.csv"] = """date,time,category,activity,duration_minutes,notes
2024-01-15,09:00,learning,Python variables,45,Completed fundamentals module
2024-01-15,10:00,coding,Built log analyzer,90,First mini project complete
2024-01-15,14:00,learning,Git and GitHub,30,Learned commit and push
2024-01-16,09:00,learning,Loops and iteration,60,for while range enumerate
2024-01-16,11:00,coding,Grade processor project,75,CSV parsing and report generation
2024-01-16,15:00,review,Code review and cleanup,30,Improved function names
2024-01-17,09:00,learning,Dictionaries and JSON,60,Nested structures and comprehensions
2024-01-17,11:00,coding,Server inventory manager,90,JSON loading and grouping
2024-01-17,14:00,learning,Exception handling,45,Custom exceptions and defensive patterns""".strip()

files["mini_projects/activity_logger/activity_logger.py"] = """
import csv
from pathlib import Path
from datetime import datetime

LOG_FILE = Path("mini_projects/activity_logger/sample_activities.csv")
VALID_CATEGORIES = ["learning", "coding", "review", "debugging", "reading"]


def load_activities(filepath):
    if not filepath.exists():
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            activities = []
            for row in reader:
                row["duration_minutes"] = int(row["duration_minutes"])
                activities.append(row)
        return activities
    except Exception as e:
        print(f"  Error loading activities: {e}")
        return []


def log_activity(filepath, category, activity, duration_minutes, notes=""):
    if category not in VALID_CATEGORIES:
        raise ValueError(
            f"Invalid category. Must be one of: {VALID_CATEGORIES}"
        )
    if duration_minutes <= 0:
        raise ValueError("Duration must be a positive number of minutes.")
    now = datetime.now()
    file_exists = filepath.exists()
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        fieldnames = ["date", "time", "category", "activity", "duration_minutes", "notes"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date":             now.strftime("%Y-%m-%d"),
            "time":             now.strftime("%H:%M"),
            "category":         category,
            "activity":         activity,
            "duration_minutes": duration_minutes,
            "notes":            notes,
        })
    print(f"  Logged: [{category}] {activity} ({duration_minutes} min)")


def get_summary(activities):
    if not activities:
        return {}
    total_minutes = sum(a["duration_minutes"] for a in activities)
    by_category = {}
    for a in activities:
        by_category.setdefault(a["category"], 0)
        by_category[a["category"]] += a["duration_minutes"]
    by_date = {}
    for a in activities:
        by_date.setdefault(a["date"], 0)
        by_date[a["date"]] += a["duration_minutes"]
    most_productive = max(by_date, key=lambda d: by_date[d])
    return {
        "total_activities": len(activities),
        "total_minutes":    total_minutes,
        "total_hours":      round(total_minutes / 60, 2),
        "by_category":      by_category,
        "by_date":          by_date,
        "most_productive":  most_productive,
        "peak_minutes":     by_date[most_productive],
    }


def generate_report(activities):
    if not activities:
        print("No activities recorded yet.")
        return
    summary = get_summary(activities)
    print("=" * 52)
    print("       ACTIVITY LOG REPORT")
    print("=" * 52)
    print(f"  Total sessions  : {summary['total_activities']}")
    print(f"  Total time      : {summary['total_minutes']} min ({summary['total_hours']} hrs)")
    print(f"  Most productive : {summary['most_productive']} ({summary['peak_minutes']} min)")
    print("\\n  TIME BY CATEGORY:")
    for category, minutes in sorted(summary["by_category"].items()):
        bar = "=" * int(minutes / 15)
        print(f"    {category:<12} {minutes:>4} min  {bar}")
    print("\\n  DAILY BREAKDOWN:")
    for date, minutes in sorted(summary["by_date"].items()):
        print(f"    {date}  {minutes:>4} min")
    print("\\n  RECENT SESSIONS (last 5):")
    for a in activities[-5:]:
        print(
            f"    {a['date']} {a['time']}  "
            f"[{a['category']}] {a['activity']} "
            f"({a['duration_minutes']} min)"
        )
    print("=" * 52)


if __name__ == "__main__":
    print("Loading activity log...\\n")
    activities = load_activities(LOG_FILE)
    print("Logging new activity...")
    try:
        log_activity(
            LOG_FILE,
            category="learning",
            activity="File handling and pathlib",
            duration_minutes=60,
            notes="Day 6 complete"
        )
    except ValueError as e:
        print(f"  Logging error: {e}")
    activities = load_activities(LOG_FILE)
    print()
    generate_report(activities)
""".strip()


for filepath, content in files.items():
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Created: {filepath}")

print("\nAll Day 6 files created successfully.")