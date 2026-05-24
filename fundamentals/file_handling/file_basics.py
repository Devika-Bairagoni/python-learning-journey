from pathlib import Path

output_path = Path("fundamentals/file_handling/sample_output.txt")

print("=== Writing a file ===")
with open(output_path, "w", encoding="utf-8") as f:
    f.write("Line 1: Server started\n")
    f.write("Line 2: Database connected\n")
    f.write("Line 3: Listening on port 8000\n")
print(f"  Written to: {output_path}")

print("\n=== Reading entire file ===")
with open(output_path, "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

print("=== Reading line by line ===")
with open(output_path, "r", encoding="utf-8") as f:
    for line_number, line in enumerate(f, start=1):
        print(f"  [{line_number}] {line.strip()}")

print("\n=== Appending to file ===")
with open(output_path, "a", encoding="utf-8") as f:
    f.write("Line 4: New connection accepted\n")
    f.write("Line 5: Request processed\n")
with open(output_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"  File now has {len(lines)} lines")

print("\n=== Safe file access ===")
missing_path = Path("does_not_exist.txt")
if missing_path.exists():
    with open(missing_path, "r", encoding="utf-8") as f:
        print(f.read())
else:
    print(f"  File not found: {missing_path}")
    print("  Skipping read operation safely.")

print("\nfile_basics.py executed successfully.")