"""
main.py

Entry point for the user management system.
Demonstrates all UserService operations with a full report.

Usage:
    python mini_projects/user_management_db/main.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mini_projects.user_management_db.user_service import UserService


def print_user_table(users):
    print(f"  {'ID':<4} {'Username':<12} {'Email':<28} {'Role':<8} {'Active'}")
    print("  " + "-" * 60)
    for user in users:
        active = "Yes" if user["active"] else "No"
        print(
            f"  {user['id']:<4} {user['username']:<12} "
            f"{user['email']:<28} {user['role']:<8} {active}"
        )


def main():
    service = UserService()

    print("=" * 58)
    print("  USER MANAGEMENT SYSTEM")
    print("=" * 58)

    # Create users
    print("\n-- Creating Users --")
    try:
        alice = service.create_user("alice", "alice@company.com", "securepass1", "admin")
        print(f"  Created: {alice['username']} (id={alice['id']})")

        bob = service.create_user("bob", "bob@company.com", "securepass2")
        print(f"  Created: {bob['username']} (id={bob['id']})")

        carol = service.create_user("carol", "carol@company.com", "securepass3")
        print(f"  Created: {carol['username']} (id={carol['id']})")

        diana = service.create_user("diana", "diana@company.com", "securepass4")
        print(f"  Created: {diana['username']} (id={diana['id']})")

    except ValueError as e:
        print(f"  Note: {e} (already seeded)")

    # Duplicate check
    print("\n-- Duplicate User Test --")
    try:
        service.create_user("alice", "alice@company.com", "newpass123")
    except ValueError as e:
        print(f"  Caught expected error: {e}")

    # List all users
    print("\n-- All Active Users --")
    users = service.get_all_users()
    print_user_table(users)

    # Update role
    print("\n-- Updating Bob to Editor --")
    try:
        updated = service.update_user_role(
            user_id=2,
            new_role="editor",
            changed_by_id=1
        )
        print(f"  Bob's new role: {updated['role']}")
    except ValueError as e:
        print(f"  Error: {e}")

    # Deactivate user
    print("\n-- Deactivating Carol --")
    try:
        service.deactivate_user(user_id=3)
        print(f"  Carol deactivated.")
    except ValueError as e:
        print(f"  Error: {e}")

    # Show active users only
    print("\n-- Active Users After Deactivation --")
    active_users = service.get_all_users(active_only=True)
    print_user_table(active_users)

    # Audit log
    print("\n-- Audit Log --")
    audit = service.get_audit_log(limit=10)
    for entry in audit:
        print(
            f"  [{entry['timestamp']}] "
            f"{entry['action']:<20} "
            f"{entry['details']}"
        )

    print("\n" + "=" * 58)
    print(f"  Database saved to: mini_projects/user_management_db/users.db")
    print("=" * 58)


if __name__ == "__main__":
    main()