# tests/test_install_marker.py
import os
from pathlib import Path
import lockam.core.install_marker as marker

def test_install_marker(tmp_path, monkeypatch):
    """ Test that the install marker file works as expected."""
    fake_marker = tmp_path / ".installed"
    monkeypatch.setattr(marker, "INSTALL_MARKER", fake_marker)

    # Initially should be fresh (file not exists)
    assert marker.is_fresh_install() is True

    # Mark as installed
    marker.mark_installed()
    assert fake_marker.exists()

    # After marking, should no longer be fresh
    assert marker.is_fresh_install() is False

    # Check file consent
    content = fake_marker.read_text()
    assert "Lockam installed" in content


