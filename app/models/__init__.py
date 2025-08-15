from app.models.user import User
from app.models.instructorApplication import InstructorApplication
from app.models.course import Course, CourseEnrollment
from app.models.foodTracking import Food, FoodLog # Add this line

__all__ = ['User', 'InstructorApplication', 'Course', 'CourseEnrollment', 'Food', 'FoodLog']