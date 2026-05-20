"""
Module: memory_reference_demo
Purpose:
Demonstrates Python variable assignment,
memory references, and dynamic typing.
"""

student_name = "Devika"
student_age = 20
is_enrolled = True

print(f"Student Name: {student_name}")
print(f"Student Age: {student_age}")
print(f"Enrollment Status: {is_enrolled}")

print("\nMemory Addresses:")

print(id(student_name))
print(id(student_age))
print(id(is_enrolled))