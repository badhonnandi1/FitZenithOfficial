from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hello350'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/fitnessSchool"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db) 

    from app.routes.auth import auth_bp
    from app.routes.routes import main_bp
    from app.routes.marathon import marathon_bp
    from app.routes.instructorRou import instructor_bp
    from app.routes.course import course_bp
    from app.routes.foodTracking import food_tracking_bp 
    from app.routes.community import community_bp 
    from app.routes.progressTracker import progress_tracker_bp
    from app.routes.resource import resource_bp
    from app.routes.announcement import announcement_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(marathon_bp)
    app.register_blueprint(instructor_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(food_tracking_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(progress_tracker_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(announcement_bp)

    @app.context_processor
    def inject_announcement():
        from app.models.announcement import Announcement
        from flask import session
        new_announcement = None
        if 'user_id' in session:
            new_announcement = Announcement.UnseenAnnouncements(session['user_id'])
        return dict(new_announcement=new_announcement)

    with app.app_context():
        from app.models.user import User
        from app.models.marathon import Marathon, MarathonRegistration
        from app.models.instructorApplication import InstructorApplication
        from app.models.course import Course, CourseEnrollment
        from app.models.foodTracking import Food, FoodLog 
        from app.models.community import Post, Comment
        from app.models.fitnessActivity import FitnessActivity
        from app.models.resource import Resource
        from app.models.announcement import Announcement, UserAnnouncementSeen
        db.create_all()

        if not Food.query.first():
            from .utils import load_sample_food_data
            load_sample_food_data()

    return app