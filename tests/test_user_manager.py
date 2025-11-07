# Lockam - Unit Tests for single-user user_manager.py
# tests/test_user_manager.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import pytest
from pathlib import Path
from lockam.core.user_manager import UserManager


@pytest.fixture
def user_manager(tmp_path):
    """ Create a fresh in-memory UserManager for each test. """
    db_path = tmp_path / "local.db"
    return UserManager(db_path)


def test_save_and_authenticate_user(user_manager):
    """Should save user and authenticate correctly."""
    user_manager.save_user("admin", "mypassword")
    assert user_manager.is_user_registered() is True
    assert user_manager.get_local_username() == "admin"
    assert user_manager.authenticate("mypassword") is True
    assert user_manager.authenticate("wrong") is False


def test_save_overwrites_existing_user(user_manager):
    """Saving again should overwrite previous user."""
    user_manager.save_user("first", "123")
    user_manager.save_user("second", "456")
    assert user_manager.get_local_username() == "second"
    assert user_manager.authenticate("456") is True
    assert user_manager.authenticate("123") is False


def test_export_user_info(user_manager):
    """Should export correct non-sensitive info."""
    user_manager.save_user("alice", "pass")
    info = user_manager.export_user_info()
    assert "username" in info
    assert "os" in info
    assert info["username"] == "alice"


def test_export_user_info_json(user_manager):
    """Should export info as JSON string."""
    user_manager.save_user("bob", "pass")
    data_json = user_manager.export_user_info_json()
    assert isinstance(data_json, str)
    assert "bob" in data_json


def test_authenticate_without_user(user_manager):
    """Should return False when no user exists."""
    assert user_manager.authenticate("any") is False
