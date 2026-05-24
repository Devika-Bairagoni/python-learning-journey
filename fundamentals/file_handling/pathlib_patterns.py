from pathlib import Path

print("=== Creating Paths ===")
project_root = Path(".")
logs_dir = project_root / "fundamentals" / "file_handling"
output_file = logs_dir / "pathlib_output.txt"
print(f"  Project root : {project_root.resolve()}")
print(f"  Logs dir     : {logs_dir}")
print(f"  Output file  : {output_file}")

print("\n=== Path Properties ===")
sample = Path("mini_projects/config_loader/config_valid.json")
print(f"  Name     : {sample.name}")
print(f"  Stem     : {sample.stem}")
print(f"  Suffix   : {sample.suffix}")
print(f"  Parent   : {sample.parent}")
print(f"  Exists   : {sample.exists()}")

print("\n=== Creating Directories ===")
new_dir = Path("fundamentals/file_handling/test_output")
new_dir.mkdir(parents=True, exist_ok=True)
print(f"  Created: {new_dir}")

print("\n=== pathlib Read/Write ===")
test_file = new_dir / "test.txt"
test_file.write_text("Hello from pathlib!\nLine 2\nLine 3", encoding="utf-8")
content = test_file.read_text(encoding="utf-8")
print(f"  Content:\n{content}")

print("\n=== Listing Python Files ===")
project = Path("fundamentals")
python_files = list(project.glob("**/*.py"))
print(f"  Python files found: {len(python_files)}")
for py_file in python_files[:5]:
    print(f"    {py_file}")

print("\n=== File Metadata ===")
config_file = Path("mini_projects/config_loader/config_valid.json")
if config_file.exists():
    stat = config_file.stat()
    size_kb = stat.st_size / 1024
    print(f"  File      : {config_file.name}")
    print(f"  Size      : {size_kb:.2f} KB")
    print(f"  Is file   : {config_file.is_file()}")
    print(f"  Is folder : {config_file.is_dir()}")

print("\npathlib_patterns.py executed successfully.")