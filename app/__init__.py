"""
Flask Application Factory for Shobhit University Gangoh Canteen System
"""

import os
from flask import Flask, render_template
from app.config import Config
from app.db import init_db, is_mongo_connected


def create_app():
    # Resolve base paths
    base_dir = os.path.abspath(os.path.dirname(__file__))
    templates_dir = os.path.join(base_dir, "templates")
    static_dir = os.path.join(base_dir, "static")

    app = Flask(
        __name__,
        template_folder=templates_dir,
        static_folder=static_dir
    )

    # Load configuration
    app.config.from_object(Config)

    # Initialize Database (MongoDB / Safe Fallback)
    with app.app_context():
        init_db(app)

    # Register Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.api_routes import api_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    # Context processors for all Jinja2 templates
    @app.context_processor
    def inject_global_data():
        return {
            "university_name": "Shobhit University Gangoh",
            "canteen_name": "SU-Gangoh Canteen Express",
            "campus_location": "Adarsh Institutional Area, Gangoh, Saharanpur (UP)",
            "is_mongo_connected": is_mongo_connected()
        }

    # Template filters
    @app.template_filter("inr")
    def inr_filter(value):
        try:
            val = float(value)
            return f"₹{val:,.2f}".rstrip("0").rstrip(".") if val % 1 == 0 else f"₹{val:,.2f}"
        except (ValueError, TypeError):
            return f"₹{value}"

    # Custom Error Pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("base.html", error_message="Page Not Found (404)"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("base.html", error_message="Internal Server Error (500)"), 500

    return app

