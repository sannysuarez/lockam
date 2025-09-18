# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/user_manager.py
# User management for Lockam (SQLite + password hashing)
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import sqlite3
from pathlib import Path
from . import utils


class UserManager:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initialize tables if not exist."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

    def add_user(self, username: str, password: str) -> bool:
        """Add new user. Returns True if success, False if username exists."""
        salt, pwd_hash = utils.hash_password(password)
        try:
            conn = self._get_conn()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, pwd_hash),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Username exists
        finally:
            conn.close()

    def authenticate(self, username: str, password: str) -> bool:
        """Check username/password. Returns True if valid."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT salt, password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return False
        salt, stored_hash = row
        return utils.verify_password(password, salt, stored_hash)

    def list_users(self):
        """Return list of all usernames."""
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users
