# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/utils.py
# Utility functions for Lockam
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

import hashlib, os, binascii


def hash_password(password: str):
    """ Generate a random salt and hash the password."""
    salt = os.urandom(16)  # 128-bit salt
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return binascii.hexlify(salt).decode("utf-8"), binascii.hexlify(pwd_hash).decode("utf-8")

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """ Verify a password against its salt and stored hash."""
    salt_bytes = binascii.unhexlify(salt.encode("utf-8"))
    pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt_bytes, 100000)
    return binascii.hexlify(pwd_hash).decode("utf-8") == stored_hash

