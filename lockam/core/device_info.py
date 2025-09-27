# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/device_info.py
# Lockam - Device Information as per install
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

'''
# Wire in device info collection so the installer sends real system info to my server during the first-time setup.
'''

import platform
import socket
import uuid
import os

def get_device_info():
    """ Collect basic device infor for server registration. """
    try:
        info = {
            "nostname": socket.gethostanme(),
            "ip_address": socket.gethostbyname(socket.gethostname()),
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "uuid": str(uuid.uuid4()), # per-install unique ID
            "user": os.getenv("USER") or os.getenv("USERNAME") or "unknown",
        }
    except Exception as e:
        info = {"error": str(e)}
        return info
