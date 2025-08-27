from app.models.user import User
from app.models.instructorApplication import InstructorApplication
from app.models.course import Course, CourseEnrollment
from app.models.foodTracking import Food, FoodLog
from app.models.fitnessActivity import FitnessActivity
from app.models.resource import Resource

__all__ = ['User', 'InstructorApplication', 'Course', 'CourseEnrollment', 'Food', 'FoodLog', 'FitnessActivity', 'Resource']