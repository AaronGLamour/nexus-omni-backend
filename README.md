# Nexus Omni — Full-Stack Secure Activity & Cloud Logging System

[![Live Demo](https://img.shields.io/badge/Live_Demo-PythonAnywhere-2ea44f?style=for-the-badge)](https://aaronglamour.pythonanywhere.com)
[![Backend](https://img.shields.io/badge/Backend-Python_Flask_&_Waitress-blue?style=for-the-badge)](https://github.com/AaronGLamour/nexus-omni-backend)
[![Frontend](https://img.shields.io/badge/Frontend-Flutter_Web-02569B?style=for-the-badge)](https://github.com/AaronGLamour/nexus-omni-frontend)

**Nexus Omni** is a self-contained, portable, and cloud-deployed full-stack web application designed for secure activity tracking, real-time filtering, and structured data reporting.

## Live Production URL
Access the live cloud deployment directly from any desktop or mobile browser:
**[https://aaronglamour.pythonanywhere.com](https://aaronglamour.pythonanywhere.com)**

## Key Features
- **Token-Based Authentication:** Secure user registration and login powered by Werkzeug password hashing and itsdangerous timed cryptographic tokens.
- **Full CRUD & Activity Logging:** Create, read, update, delete, and bulk-clear timestamped records per authenticated user.
- **Data Portability & Reporting:** Export user records as formatted JSON backups or UTF-8 CSV/Excel reports, and restore/merge data via JSON file upload with duplicate detection.
- **Portable Production Architecture:** Bundles the compiled Flutter Web production build (web_app/) directly inside the Flask/Waitress server with dynamic path resolution.

## Local Quick Start
1. Clone: git clone https://github.com/AaronGLamour/nexus-omni-backend.git
2. Install: pip install -r requirements.txt
3. Run: Double-click start_nexus.bat (Windows) or run python3 main.py (Linux/macOS).
