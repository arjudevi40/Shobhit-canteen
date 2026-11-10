"""
Authentication Routes for Shobhit University Gangoh Canteen System
Handles login for Students, Faculty, and Canteen Administrators with fallback credentials.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.config import Config
from app.db import get_collection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, redirect to appropriate home
    if "user_email" in session:
        if session.get("user_role") == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("student.menu"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        role_select = request.form.get("role_hint", "").strip().lower()

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template("login.html", email=email)

        # 1. First check against fixed sample credentials (guaranteed zero dependency startup)
        sample_creds = Config.SAMPLE_CREDENTIALS
        matched_user = None

        if email in sample_creds and sample_creds[email]["password"] == password:
            matched_user = {
                "email": email,
                "name": sample_creds[email]["name"],
                "role": sample_creds[email]["role"],
                "department": sample_creds[email].get("department", "SU-Gangoh"),
                "roll_no": sample_creds[email].get("roll_no", "SUG-2024"),
                "phone": sample_creds[email].get("phone", "+91 98765 00000")
            }
        else:
            # 2. Check against database collection
            users_col = get_collection("users")
            db_user = users_col.find_one({"email": email})
            if db_user and db_user.get("password") == password:
                matched_user = {
                    "email": db_user.get("email"),
                    "name": db_user.get("name"),
                    "role": db_user.get("role", "student"),
                    "department": db_user.get("department", "SU-Gangoh"),
                    "roll_no": db_user.get("roll_no", "SUG-2024"),
                    "phone": db_user.get("phone", "+91 98765 00000")
                }

        if matched_user:
            session.clear()
            session["user_email"] = matched_user["email"]
            session["user_name"] = matched_user["name"]
            session["user_role"] = matched_user["role"]
            session["department"] = matched_user.get("department", "")
            session["roll_no"] = matched_user.get("roll_no", "")
            session["phone"] = matched_user.get("phone", "")

            flash(f"Welcome back, {matched_user['name']}! Login successful.", "success")

            # Role-based redirection
            if matched_user["role"] == "admin":
                return redirect(url_for("admin.dashboard"))
            else:
                return redirect(url_for("student.menu"))
        else:
            flash("Invalid credentials! Please verify email and password or use the demo credentials.", "danger")
            return render_template("login.html", email=email)

    return render_template("login.html")


@auth_bp.route("/demo-login/<role>")
def demo_login(role):
    """Convenient one-click quick login for testing."""
    session.clear()
    sample_creds = Config.SAMPLE_CREDENTIALS

    if role == "admin":
        data = sample_creds["admin@shobhit.ac.in"]
        session["user_email"] = "admin@shobhit.ac.in"
        session["user_name"] = data["name"]
        session["user_role"] = "admin"
        session["department"] = data["department"]
        session["roll_no"] = "FAC-ADM-01"
        session["phone"] = data["phone"]
        flash(f"Logged in as Administrator ({data['name']})", "info")
        return redirect(url_for("admin.dashboard"))

    elif role == "staff":
        data = sample_creds["staff@shobhit.ac.in"]
        session["user_email"] = "staff@shobhit.ac.in"
        session["user_name"] = data["name"]
        session["user_role"] = "student"
        session["department"] = data["department"]
        session["roll_no"] = data["roll_no"]
        session["phone"] = data["phone"]
        flash(f"Logged in as Staff ({data['name']})", "info")
        return redirect(url_for("student.menu"))

    else: # student
        data = sample_creds["student@shobhit.ac.in"]
        session["user_email"] = "student@shobhit.ac.in"
        session["user_name"] = data["name"]
        session["user_role"] = "student"
        session["department"] = data["department"]
        session["roll_no"] = data["roll_no"]
        session["phone"] = data["phone"]
        flash(f"Logged in as Student ({data['name']})", "info")
        return redirect(url_for("student.menu"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("auth.login"))

