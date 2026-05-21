"""
grade_processor.py

Processes student grade data from a CSV-style text file.
Calculates averages, assigns letter grades, identifies at-risk students,
and generates a formatted class report.

Real-world relevance:
  - Same pattern used in educational platforms (Coursera, Google Classroom)
  - CSV processing is the foundation of all data pipelines
  - Report generation appears in every analytics backend

Usage:
    python mini_projects/grade_processor/grade_processor.py

Author: [Your Name]
Date: [Today's Date]
"""


def parse_student_data(filepath: str) -> list:
    """
    Read student file and return list of student dictionaries.

    Each student dict has keys: 'name', 'scores', 'average', 'grade'

    File format expected:
        Name,score1,score2,score3,...
    """
    students = []

    try:
        with open(filepath, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # skip empty lines

                parts = line.split(",")         # split by comma
                name = parts[0]                 # first part is the name
                # remaining parts are scores — convert from string to int
                scores = [int(score) for score in parts[1:]]

                average = sum(scores) / len(scores)

                student = {
                    "name": name,
                    "scores": scores,
                    "average": round(average, 2),
                    "grade": get_letter_grade(average),
                }
                students.append(student)

    except FileNotFoundError:
        print(f"ERROR: File not found — {filepath}")

    return students


def get_letter_grade(average: float) -> str:
    """Convert numeric average to letter grade."""
    if average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"


def get_class_average(students: list) -> float:
    """Calculate overall class average across all students."""
    if not students:
        return 0.0
    total = sum(student["average"] for student in students)
    return round(total / len(students), 2)


def get_top_students(students: list, n: int = 3) -> list:
    """Return top N students sorted by average, highest first."""
    return sorted(students, key=lambda s: s["average"], reverse=True)[:n]


def get_at_risk_students(students: list, threshold: float = 70.0) -> list:
    """Return students whose average is below the threshold."""
    return [s for s in students if s["average"] < threshold]


def generate_report(students: list) -> None:
    """Print a full class performance report."""
    if not students:
        print("No student data to report.")
        return

    class_avg = get_class_average(students)
    top_students = get_top_students(students)
    at_risk = get_at_risk_students(students)

    # --- Header ---
    print("=" * 55)
    print("       STUDENT GRADE REPORT")
    print("=" * 55)
    print(f"  Students enrolled : {len(students)}")
    print(f"  Class average     : {class_avg}%")
    print(f"  At-risk students  : {len(at_risk)}")
    print("=" * 55)

    # --- Full roster ---
    print("\n  FULL ROSTER:")
    print(f"  {'Name':<12} {'Avg':>6}  {'Grade':>6}  {'Scores'}")
    print("  " + "-" * 50)

    for student in students:
        scores_str = ", ".join(str(s) for s in student["scores"])
        print(
            f"  {student['name']:<12} "
            f"{student['average']:>6.1f}  "
            f"{student['grade']:>6}  "
            f"{scores_str}"
        )

    # --- Top performers ---
    print("\n  TOP PERFORMERS:")
    for rank, student in enumerate(top_students, start=1):
        print(f"    #{rank} {student['name']} — {student['average']}% ({student['grade']})")

    # --- At-risk alert ---
    if at_risk:
        print(f"\n  ⚠ AT-RISK STUDENTS (avg < 70%):")
        for student in at_risk:
            print(f"    • {student['name']} — {student['average']}% ({student['grade']})")
    else:
        print("\n  ✓ No at-risk students. Class performing well.")

    print("=" * 55)


if __name__ == "__main__":
    FILE_PATH = "mini_projects/grade_processor/students.txt"

    print(f"Loading student data from: {FILE_PATH}\n")
    students = parse_student_data(FILE_PATH)
    generate_report(students)