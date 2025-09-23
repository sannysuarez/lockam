# Lockam - PC Intrusion Detection & Auto-Lock Software
# run.py - Entry point for Lockam demo/testing
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

from lockam import create_app
from gui import setup_wizard
from lockam.core.install_marker import is_fresh_install

def main():
    app = create_app()
    um = app["user_manager"]

    print("Lockam started successfully!")
    print(f"Using database at: {app['db_path']}\n")


    # Only show Setup Wizard if fresh install
    if is_fresh_install():
        setup_wizard.run_setup_wizard(um)
    else:
        print("Lockam is already installed. Launching main app...")
        # TODO: Replace this with main dashboard/lock screen later


if __name__ == "__main__":
    main()

