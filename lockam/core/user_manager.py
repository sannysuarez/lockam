# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/user_manager.py
# User management for Lockam (Handles one local user per device (no remote control, no multi-user system))
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import sqlite3
from pathlib import Path
import json
import platform
from datetime import datetime, timezone
from . import utils


class UserManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize local user table (single user only)."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS local_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def save_user(self, username: str, password: str) -> bool:
        """Store or update local user credentials."""
        salt, pwd_hash = utils.hash_password(password)
        conn = self._get_conn()
        cursor = conn.cursor()

        # Only one local user record — replace if exists
        cursor.execute("DELETE FROM local_user")
        cursor.execute(
            "INSERT INTO local_user (username, salt, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, salt, pwd_hash, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        conn.close()
        return True

    def authenticate(self, password: str) -> bool:
        """Verify password for local user."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT salt, password_hash FROM local_user LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False

        salt, stored_hash = row
        return utils.verify_password(password, salt, stored_hash)

    def get_local_username(self) -> str | None:
        """Return the stored local username."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM local_user LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def is_user_registered(self) -> bool:
        """Check if a local user already exists."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM local_user")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0

    def export_user_info(self) -> dict:
        """
        Export non-sensitive user info for reporting or remote documentation.
        Returns a JSON-safe dict that can be sent to a remote API.
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT username, created_at FROM local_user LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {}

        username, created_at = row
        info = {
            "username": username,
            "system_name": platform.node(),
            "os": platform.system(),
            "os_version": platform.version(),
            "registered_at": created_at,
        }
        return info

    def export_user_info_json(self) -> str:
        """Convenience: return export info as JSON string."""
        return json.dumps(self.export_user_info(), indent=2)
