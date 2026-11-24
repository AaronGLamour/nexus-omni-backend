@'
# Nexus Omni - Secure Activity & Data Management System

A full-stack Client-Server system combining a **Python (Flask)** backend with a production **Flutter Web** frontend served from a single unified endpoint (`http://127.0.0.1:5000`).

## Key Features
- **Authentication & Encryption:** Password hashing (`Werkzeug PBKDF2`) and signed time-limited tokens (`itsdangerous`, 24h validity).
- **Multi-Tenant Data Isolation:** Complete separation of records per user account.
- **Full CRUD Operations:** Create, read, update, and delete activity logs with automatic timestamps.
- **Analytics & Filtering:** Real-time summary cards, instant search, and dynamic app filter chips.
- **Backup & Reporting:**
  - Export and restore **JSON** backups with duplicate prevention.
  - Export **Excel (CSV)** reports with `UTF-8 BOM` encoding.
  - Safe `Clear All` option per user account with confirmation dialog.

## Tech Stack
- **Backend:** Python 3, Flask, Flask-SQLAlchemy, Flask-CORS, SQLite
- **Frontend:** Flutter Web (Material Design, RTL Support, HTTP)
- **Security:** Signed Tokens (`itsdangerous`), Environment Variables (`.env`)

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
