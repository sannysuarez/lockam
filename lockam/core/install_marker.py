# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/install_marker.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

'''
# On fresh install - Wizard runs.
# After wizard submits & syncs with server - mark_installed() ensures .installed file exists.
# On next runs - app skips wizard and goes to main window.
'''

from pathlib import Path

INSTALL_MARKER = Path("lockam/storage/.installed")

def is_fresh_install():
    return not INSTALL_MARKER.exists()

def mark_installed():
    INSTALL_MARKER.parent.mkdir(parents=True, exist_ok=True)
    with open(INSTALL_MARKER, "w") as f:
        f.write("Lockam installed\n")
