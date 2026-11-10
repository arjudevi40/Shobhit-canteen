#!/usr/bin/env python3
"""
WSGI Application Entry Point
Shobhit University Gangoh - Canteen Management System

To run the application:
    python wsgi.py
"""

import sys
import os
from app import create_app
from app.config import Config

app = create_app()

if __name__ == "__main__":
    host = Config.HOST
    port = Config.PORT
    debug = Config.DEBUG

    print("=" * 70)
    print("  SHOBHIT UNIVERSITY GANGOH - CANTEEN MANAGEMENT SYSTEM")
    print("  Portal: SU-Gangoh Canteen Express")
    print(f"  Access URL: http://{host}:{port}/")
    print("=" * 70)
    print("  Default Test Logins:")
    print("    - Admin:   admin@shobhit.ac.in   / admin123")
    print("    - Student: student@shobhit.ac.in / student123")
    print("    - Staff:   staff@shobhit.ac.in   / staff123")
    print("=" * 70)

    app.run(host=host, port=port, debug=debug)

