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
    print("\n  TIME BY CATEGORY:")
    for category, minutes in sorted(summary["by_category"].items()):
        bar = "=" * int(minutes / 15)
        print(f"    {category:<12} {minutes:>4} min  {bar}")
    print("\n  DAILY BREAKDOWN:")
    for date, minutes in sorted(summary["by_date"].items()):
        print(f"    {date}  {minutes:>4} min")
    print("\n  RECENT SESSIONS (last 5):")
    for a in activities[-5:]:
        print(
            f"    {a['date']} {a['time']}  "
            f"[{a['category']}] {a['activity']} "
            f"({a['duration_minutes']} min)"
        )
    print("=" * 52)


if __name__ == "__main__":
    print("Loading activity log...\n")
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