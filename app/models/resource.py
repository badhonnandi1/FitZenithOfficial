from app import db
from datetime import date

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    resource_number = db.Column(db.Integer, nullable=False)
    date_uploaded = db.Column(db.Date, nullable=False, default=date.today)
    file_path = db.Column(db.String(300), nullable=False)

    course = db.relationship('Course', backref='resources', lazy=True)
    instructor = db.relationship('User', backref='resources', lazy=True)

    @staticmethod
    def get_by_course(course_id):
        return Resource.query.filter_by(course_id=course_id).order_by(Resource.resource_number).all()

    @staticmethod
    def get_by_id(resource_id):
        return Resource.query.get_or_404(resource_id)

    @staticmethod
    def create(course_id, instructor_id, title, resource_number, file_path):
        new_resource = Resource(
            course_id=course_id,
            instructor_id=instructor_id,
            title=title,
            resource_number=resource_number,
            file_path=file_path
        )
        db.session.add(new_resource)
        db.session.commit()
        return new_resource

    @staticmethod
    def delete(resource_id):
        resource = Resource.get_by_id(resource_id)
        if resource:
            db.session.delete(resource)
            db.session.commit()
            return True
        return False