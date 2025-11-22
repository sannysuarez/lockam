# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/validators.py
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

"""
This module contains input validation functions for the Lockam setup wizard.
All functions return (bool, str):
 - bool -> True if valid
 - str  -> error message, or "" if valid
"""

from datetime import date
import re


def validate_fullname(name: str):
    """Validate full name: 3–50 chars, letters, numbers, space, '.', '-', ' allowed."""
    name = name.strip()

    # FIXED: removed space in {3,50}
    if not re.match(r"^[A-Za-z0-9 .'-]{3,50}$", name):
        return False, "Invalid full name format."

    return True, ""


def validate_email(email: str):
    """Validate email format. Empty email is allowed."""
    email = email.strip()

    if email == "":
        return True, ""

    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False, "Invalid email address."

    return True, ""


def validate_username(username: str):
    """Validate username: 3–32 chars, alphanumeric + _ - ."""
    username = username.strip()

    # FIXED: removed space in {3,32}
    if not re.match(r"^[A-Za-z0-9_.-]{3,32}$", username):
        return False, "Username must be 3-32 characters (letters, numbers, _, ., -)."

    return True, ""


def validate_password(password: str):
    """Validate password: min 6 chars, no spaces."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."

    if " " in password:
        return False, "Password cannot contain spaces."

    return True, ""


def validate_dob(dob: date, min_age_years=5):
    """
    Validate date of birth:
     - must not be in the future
     - must be >= min_age_years old
    """
    today = date.today()

    if dob > today:
        return False, "Date of birth cannot be in the future."

    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    if age < min_age_years:
        return False, f"User must be at least {min_age_years} years old."

    return True, ""


def validate_inputs(fullname, email, username, password, dob):
    """Run all validators and return first error found."""
    checks = [
        (validate_fullname, fullname),
        (validate_email, email),
        (validate_username, username),
        (validate_password, password),
        (validate_dob, dob),
    ]

    for fn, value in checks:
        valid, msg = fn(value)
        if not valid:
            return False, msg

    return True, ""
