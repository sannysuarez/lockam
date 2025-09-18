# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/__init__.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import os
from pathlib import Path
from .core import user_manager

__version__ = "1.0.0"
__author__ = "Muhammad Sanni"


def create_app():
    """ Application factory for lockam. """
    # Ensure storage directory exists
    storage_path = Path(__file__).resolve().parent / "storage"
    storage_path.mkdir(exist_ok=True)

    # Database path
    db_path = storage_path / "lockam.db"

    # Application context
    app = {
        "db_path": db_path,
        "user_manager": user_manager.UserManager(db_path),
    }
    return app
