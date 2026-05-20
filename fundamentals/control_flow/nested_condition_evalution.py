"""
Nested condition example.
"""

age = 20
has_id_card = True

if age >= 18:

    if has_id_card:
        print("Entry Allowed")

    else:
        print("ID Card Required")

else:
    print("Underage")