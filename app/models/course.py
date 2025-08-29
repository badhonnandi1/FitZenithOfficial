from app import db
from datetime import datetime
from sqlalchemy import text
from app.models.user import User

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    duration = db.Column(db.String(50), nullable=False) 
    price = db.Column(db.Float, nullable=False, default=0.0)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    materials = db.Column(db.Text, nullable=True) 

    instructor = db.relationship('User', backref='courses', lazy=True)
    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def createCourse(form_data, instructor_id):
        new_course = Course(
            title=form_data.get('title'),
            description=form_data.get('description'),
            duration=form_data.get('duration'),
            price=float(form_data.get('price', 0)),
            instructor_id=instructor_id,
            materials=form_data.get('materials')
        )
        db.session.add(new_course)
        db.session.commit()
        return new_course

    @staticmethod
    def AllCourses():
        return Course.query.all()
    
    @staticmethod
    def getCourseByID(id):
        return Course.query.get(id)

    @staticmethod
    def deleteCourse(course_id):
        course = Course.query.get(course_id)
        if course:
            db.session.delete(course)
            db.session.commit()

class CourseEnrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrollment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def enroll_user(user_id, course_id):
        existing_enrollment = CourseEnrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        if existing_enrollment:
            return False, "You are already enrolled in this course."
        
        enrollment = CourseEnrollment(user_id=user_id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        return True, "Successfully enrolled in the course!"
    
    @staticmethod
    def is_enrolled(user_id, course_id):
        result = CourseEnrollment.query.filter_by(user_id=user_id, course_id=course_id).first()
        return True if result else False

  