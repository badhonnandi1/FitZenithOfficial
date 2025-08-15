from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hello350'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/fitnessSchool"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.routes import main_bp
    from app.routes.marathon import marathon_bp
    from app.routes.instructorRou import instructor_bp
    from app.routes.course import course_bp
    from app.routes.foodTracking import food_tracking_bp 
    from app.routes.community import community_bp 
    from app.models.community import Post, Comment

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(marathon_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(food_tracking_bp)
    app.register_blueprint(community_bp)
    
    with app.app_context():
        from app.models.user import User
        from app.models.marathon import Marathon, MarathonRegistration
        from app.models.instructorApplication import InstructorApplication
        from app.models.course import Course, CourseEnrollment
        from app.models.foodTracking import Food, FoodLog 
        db.create_all()

        # Add sample food data
        if not Food.query.first():
            from .utils import load_sample_food_data
            load_sample_food_data()

    return app