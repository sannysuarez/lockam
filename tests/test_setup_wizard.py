# Lockam - Unit Tests for slockam/core/validators.py
# tests/test_user_manager.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.
"""
Covers:
 - Fullname validation
 - Email validation
 - Username Validation
 - Password validation
 - Date of birth validation
 - Combined validation_inputs()
"""
import pytest
from datetime import date, timedelta
from lockam.core.validators import (
    validate_fullname,
    validate_email,
    validate_username,
    validate_password,
    validate_dob,
    validate_inputs
)

# -------------------------------------------------
# FULL NAME TESTS
# -------------------------------------------------
def test_fullname_valid():
    valid, msg = validate_fullname("Sanni Suarez")
    assert valid is True
    assert msg == ""

def test_fullname_invalid_short():
    valid, msg = validate_fullname("Sa")
    assert not valid
    assert "Invalid full name" in msg

def test_fullname_invalid_characters():
    valid, msg = validate_fullname("sanni@suarez")
    assert not valid

# -------------------------------------------------
# EMAIL TESTS
# -------------------------------------------------
def test_email_valid():
    valid, msg = validate_email("user@example.com")
    assert valid is True

def test_email_invalid_format():
    valid, msg = validate_email("invalid-email")
    assert not valid
    assert "Invalid email" in msg

def test_email_empty_is_allowed():
    valid, msg = validate_email("")
    assert valid is True #email is optional

# ------------------------------------------------
# USERNAME TESTS
# ------------------------------------------------
def test_username_valid():
    valid, msg = validate_username("Sanni_suarez")
    assert valid is True

def test_username_too_short():
    valid, msg = validate_username("ab")
    assert not valid

def test_username_invalid_characters():
    valid, msg = validate_username("Bad Username!")
    assert not valid

# -------------------------------------------------------
# PASSWORD TESTS
# -------------------------------------------------------
def test_password_valid():
    valid, msg = validate_password("secret123")
    assert valid is True

def test_password_too_short():
    valid, msg = validate_password("123")
    assert not valid
    assert "6 characters" in msg

def test_password_has_spaces():
    valid, msg = validate_password("pass word")
    assert not valid
    assert "spaces" in msg

# ------------------------------------------------------
# DATE OF BIRTH (DOB) TESTS
# ------------------------------------------------------
def test_dob_valid_age():
    dob = date.today().replace(year=date.today().year - 20)
    valid, msg = validate_dob(dob)
    assert valid is True

def test_dob_in_future():
    dob = date.today() + timedelta(days=5)
    valid, msg = validate_dob(dob)
    assert not valid
    assert "future" in msg

def test_dob_too_young():
    dob = date.today().replace(year=date.today().year- 2)
    valid, msg = validate_dob(dob, min_age_years=5)
    assert not valid
    assert "5 years" in msg

# ----------------------------------------------------------
# COMBINED VALIDATION TESTS
# ----------------------------------------------------------
def test_validate_inputs_all_valid():
    dob = date.today().replace(year=date.today().year - 25)

    valid, msg = validate_inputs(
        fullname="Sanni Suarez",
        email="sanni@example.com",
        username="Sanni123",
        password="password",
        dob=dob
    )
    assert valid is True
    assert msg == ""

def test_validate_inputs_first_failure_fullname():
    dob = date.today().replace(year=date.today().year -25)

    valid, msg = validate_inputs(
        fullname="S!",
        email="sanni@example.com",
        username="sanni123",
        password="password",
        dob=dob
    )
    assert not valid
    assert "full name" in msg.lower()

def test_validate_inputs_failure_email():
    dob = date.today().replace(year=date.today().year - 25)

    valid, msg = validate_inputs(
        fullname="Valid Name",
        email="bad-email",
        username="sanni123",
        password="password",
        dob=dob
    )
    assert not valid
    assert "email" in msg.lower()

def test_validate_inputs_failure_username():
    dob = date.today().replace(year=date.today().year -25)

    valid, msg = validate_inputs(
        fullname="Valid Name",
        email="sanni@example.com",
        username="??bad??",
        password="password",
        dob=dob
    )
    assert not valid
    assert "username" in msg.lower()

def test_validate_inputs_failure_password():
    dob = date.today().replace(year=date.today().year - 25)

    valid, msg = validate_inputs(
        fullname="Valid Name",
        email="sanni@example.com",
        username="sanni123",
        password="12",
        dob=dob
    )
    assert not valid
    assert "password" in msg.lower()

def test_validate_inputs_failure_dob():
    dob = date.today().replace(year=date.today().year -2)

    valid, msg = validate_inputs(
        fullname="Valid Name",
        email="sanni@example.com",
        username="sanni123",
        password="password",
        dob=dob
    )
    assert not valid
    assert "years" in msg.lower()









