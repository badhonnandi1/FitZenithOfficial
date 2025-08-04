# This file makes the routes directory a Python package
# You can import all route blueprints here if needed

from app.routes.routes import main_bp
from app.routes.auth import auth_bp
# from app.routes.updateProfile import update_profile_bp
# from app.routes.auth import profile_bp

__all__ = ['main_bp', 'auth_bp']