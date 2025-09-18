# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/gui/setup_wizard.py
# Lockam - Setup Wizard (PyQt5)
# Lockam - Setup Wizard GUI
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

from PyQt5.QtWidgets  import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
import sys

def run_setup_wizard(user_manager):
    """ Launch the setup wizard window. """
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Lockam - Setup Wizard")

    layout = QVBoxLayout()

    # Welcome message
    label = QLabel("Welcome to Lockam!\nCreate your first admin account.")
    layout.addWidget(label)

    # Username field
    username_input = QLineEdit()
    username_input.setPlaceholderText("Enter admin username")
    layout.addWidget(username_input)

    # Password field
    password_input = QLineEdit()
    password_input.setPlaceholderText("Enter admin password")
    password_input.setEchoMode(QLineEdit.Password)
    layout.addWidget(password_input)

    # Submit button
    def on_submit():
        username = username_input.text().strip()
        password = password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(window, "Error", "Both fields are required!")
            return

        created = user_manager.add_user(username, password)
        if created:
            QMessageBox.information(window, "Success", f"User '{username}' created successfully!")
            window.close()
        else:
            QMessageBox.warning(window, "Error", f"User '{username}' already exists!")

    submit_btn = QPushButton("Create Admin")
    submit_btn.clicked.connect(on_submit)
    layout.addWidget(submit_btn)

    window.setLayout(layout)
    window.resize(400, 200)
    window.show()

    sys.exit(app.exec_())
