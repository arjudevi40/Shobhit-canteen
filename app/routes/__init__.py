# Routes package initialization
from app.routes.auth_routes import auth_bp
from app.routes.student_routes import student_bp
from app.routes.admin_routes import admin_bp
from app.routes.api_routes import api_bp

__all__ = ["auth_bp", "student_bp", "admin_bp", "api_bp"]

