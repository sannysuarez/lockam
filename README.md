# 🔒 Lockam – PC Intrusion Detection &amp; Auto-Lock Software  

Lockam is a standalone desktop security app built with **Python (PyQt5)** that protects your computer from unauthorized access.  

It runs silently in the background and instantly **locks your screen** when suspicious activity is detected — including unknown faces via your webcam.  

---

## ✨ Features  

- 👥 **Multiple Users** – create and manage multiple accounts with roles (admin, user, guest)  
- 🔐 **Auto-Lock** – immediately lock the system when intruders are detected  
- 📷 **Webcam Integration** – capture intruder images in real time  
- 📝 **Intrusion Logs** – record every unauthorized attempt (with timestamps & details)  
- 🛠 **Cross-Platform** – works on **Windows, Linux, and macOS**  

---

## 📂 Project Structure  

```bash
lockam/
│
├── lockam/                
│   ├── __init__.py        # app factory
│   │
│   ├── core/              
│   │   ├── __init__.py
│   │   ├── user_manager.py   # SQLite logic
│   │   ├── auth.py           # authentication helpers
│   │   ├── webcam.py         # webcam intrusion detection
│   │   ├── lockscreen.py     # lockscreen GUI (PyQt5)
│   │   └── utils.py          # helpers (hashing, config, etc.)
│   │
│   ├── gui/               
│   │   ├── __init__.py
│   │   ├── dashboard.py      # main dashboard
│   │   └── setup_wizard.py   # first-time setup
│   │
│   └── storage/
│       ├── __init__.py
│       └── lockam.db         # (ignored in git)
│
├── tests/                 
│   ├── __init__.py
│   └── test_user_manager.py
│
├── requirements.txt       
├── run.py                 
├── .gitignore             
├── LICENSE                
├── CONTRIBUTING.md        
└── README.md
```

## 📄 `LICENSE & USAGE`

Lockam – All Rights Reserved

Copyright (c) 2025 Muhammad Sanni

This software is provided for PERSONAL and NON-COMMERCIAL USE only.

You are NOT allowed to:
- Copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this Software
- Use this Software as part of another project without explicit written consent
- Create derivative or commercial works from this Software

You are allowed to:
- View and study the source code
- Use it personally on your own computer
- Contribute to this repository through Pull Requests

Contributors grant the project owner (Muhammad Sanni) the right to use, modify, and distribute their code as part of this project only.

For permissions, contact: [sannysuarez4@gmail.com]

