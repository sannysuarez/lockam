# Lockam - PC Intrusion Detection & Auto-Lock Software
# lockam/core/setup_wizard.py
# Lockam - Setup Wizard GUI (PyQt5)
# Copyright (c) 2025 Muhammad Sanni
# All rights reserved. See LICENSE for details.

# import centralized validators
from lockam.core.validators import validate_inputs

from PyQt5.QtWidgets import (
    QApplication, QWizard, QWizardPage, QLabel, QLineEdit,
    QDateEdit, QComboBox, QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import QDate
from lockam.core.install_marker import mark_installed
from lockam.core.countries import get_country_list, get_country_code
import requests
import sys

SERVER_URI = "https://lockam.sanni.com.ng/api/register_device"  # Server endpoint

class SetupWizard(QWizard):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager

        self.setWindowTitle("Lockam - One Time Setup")
        self.resize(500, 550)

        # --- Style (modern look) ---
        self.setStyleSheet("""
            QLineEdit, QComboBox, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)

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
        self.fullname.setPlaceholderText("Enter your full name")

        self.dob = QDateEdit()
        self.dob.setCalendarPopup(True)
        self.dob.setDate(QDate.currentDate().addYears(-5))

        self.country = QComboBox()
        self.country.addItems(get_country_list())

        self.gender = QComboBox()
        self.gender.addItems(["Select Gender", "Male", "Female"])

        self.email = QLineEdit()
        self.email.setPlaceholderText("Enter your email address")

        layout.addWidget(QLabel("Full Name:"))
        layout.addWidget(self.fullname)
        layout.addWidget(QLabel("Date of Birth (yyyy-mm-dd):"))
        layout.addWidget(self.dob)
        layout.addWidget(QLabel("Country:"))
        layout.addWidget(self.country)
        layout.addWidget(QLabel("Gender:"))
        layout.addWidget(self.gender)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email)

        page.setLayout(layout)
        return page

    def create_credentials_page(self):
        page = QWizardPage()
        page.setTitle("Admin Credentials")

        layout = QVBoxLayout()
        self.username = QLineEdit()
        self.username.setPlaceholderText("Choose a username")

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Choose a strong password")

        layout.addWidget(QLabel("Username:"))
        layout.addWidget(self.username)
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password)

        page.setLayout(layout)
        return page

    def create_face_enroll_page(self):
        page = QWizardPage()
        page.setTitle("Face Enrollment")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Capture your face (stub for now)..."))

        # TODO: integrate actual recognition enrollment
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
                                "- See consent details: https://lockam.sanni.com.ng/consent"
                                ))

        finish_btn = QPushButton("Finish & Submit")
        finish_btn.clicked.connect(self.finalize_setup)
        layout.addWidget(finish_btn)

        page.setLayout(layout)
        return page

    def finalize_setup(self):
        """ Validate, save user locally, send to server, mark installation complete. """
        # CENTRAL VALIDATION
        valid, message = validate_inputs(
            self.fullname.text(),
            self.email.text(),
            self.username.text(),
            self.password.text()
        )
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return


        # --- Ensure country and gender are selected ---
        if self.country.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select a country.")
            return
        if self.gender.currentIndex() == 0:
            QMessageBox.warning(self, "Validation Error", "Please select a gender.")
            return

        try:
            # 1. Save minimal info locally (username, password, face)
            self.user_manager.add_user(self.username.text().strip(), self.password.text().strip())

            # 2. Send extended info to server
            payload = {
                "fullname": self.fullname.text().strip(),
                "dob": self.dob.date().toString("yyyy-MM-dd"),
                "country": self.country.currentText(),
                "gender": self.gender.currentText(),
                "username": self.username.text().strip(),
                "email": self.email.text().strip(),
                "face_data": self.face_data,
                "device_info": "stub-device-info"  # TODO: detect real device info
            }
            try:
                r = requests.post(SERVER_URI, json=payload, timeout=10)
                r.raise_for_status()
            except Exception as e:
                QMessageBox.warning(self, "Network Error", f"Could not connect to server.\n\n{e}")
                return

            # 3. Mark installation complete
            mark_installed()

            QMessageBox.information(self, "Setup Complete",
                                    "Lockam has been installed successfully.\nYou are registered as the Admin.")
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Setup Failed", str(e))

def run_setup_wizard(user_manager):
    """ Launch the setup wizard. """
    app = QApplication(sys.argv)
    wizard = SetupWizard(user_manager)
    wizard.show()
    app.exec_()
