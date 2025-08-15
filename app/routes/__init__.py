from app.routes.routes import main_bp
from app.routes.auth import auth_bp
from app.routes.instructorRou import instructor_bp # Add this line

__all__ = ['main_bp', 'auth_bp', 'instructor_bp']