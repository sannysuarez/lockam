# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/gui/setup_wizard.py
# Lockam - Setup Wizard GUI (PyQt5)
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

from PyQt5.QtWidgets  import (QApplication, QWizard, QWizardPage, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from lockam.core.device_info import get_device_info
from lockam.core.install_marker import mark_installed, is_fresh_install
import requests
import sys

SERVER_URI = "https://lockam.sanni.com.ng/api/register_device"  # The server endpoint for device registration

class SetupWizard(QWizard):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager

        self.setWindowTitle("Lockam - First Time setup")
        self.resize(500, 350)

        # Pages
        self.addPage(self.create_user_info_page())
        self.addPage(self.create_credentials_page())
        self.addPage(self.create_face_enroll_page())
        self.addPage(self.create_summary_page())

    def create_user_info_page(self):
        page = QWizardPage()
        page.setTitle("User Information")

        layout = QVBoxLayout()
        self.fullname = QLineEdit()
        self.dob = QLineEdit()
        self.country = QLineEdit()
        self.gender = QLineEdit()
        self.email = QLineEdit()

        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.fullname)
        layout.addWidget(QLabel("Date of Birth (YYYY-MM-DD):"))
        layout.addWidget(self.dob)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country)
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender)
        layout.addWidget(QLabel("Email (optional):"))

        page.setLayout(layout)
        return page

    def create_credentials_page(self):
        page = QWizardPage()
        page.setTitle("Admin Credentials")

        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)

        layout.addWidget(QLabel("Choose a Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Choose a Password:"))
        layout.addWidget(self.password)

        page.setLayout(layout)
        return page

    def create_face_enroll_page(self):
        page = QWizardPage()
        page.setTitle("Face Enrollment")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Capture your face (stub for now)..."))

        # TODO: integrate actul recognition enrollment here
        self.face_data = "dummy_face_encoded_data"

        page.setLayout(layout)
        return page

    def create_summary_page(self):
        page = QWizardPage()
        page.setTitle("Summary & Consent")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("We will collect:\n"
                                "- Full name, DOB, Country, Gender, Email\n"
                                "- Device info (OS, hardware)\n"
                                "- Face scan (stored locally)\n"
                                "- see consent details here: https://lockam.sanni.com.ng/consent"
                                ))

        finish_btn = QPushButton("Finish & Submit")
        finish_btn.clicked.connect(self.finalize_setup)
        layout.addWidget(finish_btn)

        page.setLayout(layout)
        return page

    def finalize_setup(self):
        """ Save user locally, send extended info to server, mark installtion complete."""
        try:
            # 1. Save minimal info locally (username, password, face)
            self.user_manager.add_user(self.username.text(), self.password.text())

            # 2. Send extended info to server
            payload = {
                "fullname": self.fullname.text().strip(),
                "dob": self.dob.text().strip(),
                "country": self.country.text().strip(),
                "gender": self.gender.text().strip(),
                "username": self.username.text().strip(),
                "email": self.email.text().strip(),
                "face_data": self.face_data,
                "device_info": "stub-device-info" # TODO: detect real device info
            }
            try:
                r = requests.post(SERVER_URI, json=payload, timeout=10)
                r.raise_for_status()
            except Exception as e:
                QMessageBox.warning(self, "Network Error", f"Could not connect to server.\n\n{e}:")
                return # stop until internet is available

            # 3. Mark installation complete
            mark_installed()

            created = self.user_manager.add_user("Setup Complete", "Lockam has been installed successfully.\n You are registered as the Admin." )
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Setup Failed", str(e))

def run_setup_wizard(user_manager):
        """ Lucnh the setup wizard. """
        import sys
        app = QApplication(sys.argv)
        wizard = SetupWizard(user_manager)
        wizard.show()
        app.exec_()

