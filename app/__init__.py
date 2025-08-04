from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Application factory function"""
    app = Flask(__name__)


    app.secret_key = 'hello350'

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/fitnessSchool"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['UPLOAD_FOLDER'] = 'static/uploads' 

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.routes import main_bp
    from app.routes.marathon_routes import marathon_bp 

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(marathon_bp) 

    with app.app_context():
        from app.models.user import User
        from app.models.marathon import Marathon, MarathonRegistration
        db.create_all()

    return app
