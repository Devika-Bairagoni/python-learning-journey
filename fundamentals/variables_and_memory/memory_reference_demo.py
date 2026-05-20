"""
Module: memory_reference_demo

Purpose:
Demonstrates Python variable assignment,
memory references, and object identity.
"""

student_name = "Devika"
another_reference = student_name

print("Student Name:", student_name)

print("\nMemory Addresses:")
print(id(student_name))
print(id(another_reference))

print("\nIdentity Check:")
print(student_name is another_reference)