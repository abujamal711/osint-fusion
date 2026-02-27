#!/usr/bin/env python3
from backend.app import app

if __name__ == '__main__':
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     OSINT FUSION PLATFORM - ETHICAL USE ONLY             ║
    ║     Access at http://localhost:5000                      ║
    ║     Make sure to set API keys in .env file               ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
