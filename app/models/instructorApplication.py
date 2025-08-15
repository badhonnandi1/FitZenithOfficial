from app import db
from datetime import datetime
from sqlalchemy import text
from app.models.user import User 


class InstructorApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    years_of_experience = db.Column(db.Integer, default=0)
    reason = db.Column(db.Text, nullable=False)
    application_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending') 
    # 'pending', 'approved', 'disapproved'

    user = db.relationship('User', backref='instructor_application', lazy=True)

    @staticmethod
    def create_application(user_id, form_data):
        application = InstructorApplication(
            user_id=user_id,
            name=form_data.get('name'),
            phone=form_data.get('phone'),
            years_of_experience=int(form_data.get('years_of_experience', 0)),
            reason=form_data.get('reason')
        )
        db.session.add(application)
        db.session.commit()
        return application

    @staticmethod
    def get_all_pending():
        return InstructorApplication.query.filter_by(status='pending').all()

    @staticmethod
    def get_by_id(app_id):
        return InstructorApplication.query.get(app_id)

    def approve(self):
        self.status = 'approved'
        self.user.role = 'instructor'
        db.session.commit()

    def disapprove(self):
        self.status = 'disapproved'
        db.session.commit()
