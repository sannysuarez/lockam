# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/run.py - Entry point for Lockam demo/testing
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

from lockam import create_app

def main():
    app = create_app()
    um = app["user_manager"]

    print("Lockam started successfully!")
    print(f"Using database at: {app['db_path']}\n")


    # --- DEMO USAGE ---
    print("\n[1] Adding user 'admin' with password 'secret123'")
    created = um.add_user("admin", "secret123")
    print("User created:", created)

    print("\n[2] Current users:")
    print(um.list_users())

    print("\n[3] Authenticate with correct password:")
    print("Result:", um.authenticate("admin", "secret123"))

    print("\n[4] Authenticate with wrong password:")
    print("Result:", um.authenticate("admin", "wrongpass"))


if __name__ == "__main__":
    main()

