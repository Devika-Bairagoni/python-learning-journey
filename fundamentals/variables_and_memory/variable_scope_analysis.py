"""
Demonstrates local and global scope.
"""

global_message = "Global Scope"


def demonstrate_scope():
    local_message = "Local Scope"

    print(global_message)
    print(local_message)


demonstrate_scope()