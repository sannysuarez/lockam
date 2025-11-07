# Lockam - Unit Tests for user_manager.py
# tests/test_user_manager.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import pytest
from lockam.core.user_manager import UserManager

@pytest.fixture
def user_manager():
    """ Create a fresh in-memory UserManager for each test. """
    um = UserManager(":memory:") # temporary database
    yield um

def test_add_user_and_authenticate(user_manager):
    """ Should add user and authenticate correctly. """
    assert user_manager.add_user("admin", "seret123") is True
    assert user_manager.authenticate("admin", "secret123") is True
    assert user_manager.authenticate("admin", "wrong") is False

def test_duplicate_user_fails(user_manager):
    """ Should not allow duplicate username. """
    user_manager.add_user("john", "pass1")
    result = user_manager.add_user("john", "pass2")
    assert result is False # should not add twice

def test_list_users(user_manager):
    """ Should list all registered users. """
    user_manager.add_user("alice", "pass")
    user_manager.add_user("bob", "pass")
    users = user_manager.list_users()
    assert "alice" in users
    assert "bob" in users
    assert isinstance(users, list)

def test_remove_user(user_manager):
    """ should remove a user properly. """
    user_manager.add_user("mark", "1234")
    assert user_manager.remove_user("mark") is True
    assert "mark" not in user_manager.list_users()

def test_authenticate_case_sensitivity(user_manager):
    """ Usernames should be case-sensitive. """
    user_manager.add_user("TestUser", "abc")
    assert user_manager.authenticate("TestUser", "abc") is True
    assert user_manager.authenticate("testuser", "abc") is False





