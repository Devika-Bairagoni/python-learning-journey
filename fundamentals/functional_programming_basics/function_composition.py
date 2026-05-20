"""
Function composition example.
"""

def square_number(number):
    return number * number


def double_number(number):
    return number * 2


result = double_number(square_number(5))

print(result)