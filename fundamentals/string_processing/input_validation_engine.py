"""
Simple input validation.
"""

email = "devika@gmail.com"

if "@" in email and ".com" in email:
    print("Valid Email")

else:
    print("Invalid Email")