# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/gui/setup_wizard.py
# Lockam - Setup Wizard (PyQt5)
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

from PyQt5.QtWidgets  import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
import sys

def run_setup_wizard(user_manager):
    """ Launch the setup wizard window. """
    app = QApplication(sys.argv)

    # Simple window for now
    window = QWidget()
    window.setWindowTitle("Lockam - Setup Wizard")

    layout = QVBoxLayout()
    label = QLabel("Welcome to Lockam!\nThis is where setup will happen.")
    layout.addWidget(label)

    window.setLayout(layout)
    window.resize(400, 200)
    window.show()

    sys.exit(app.exec_())
