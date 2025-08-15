from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.course import Course, CourseEnrollment
from app.models.user import User

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses/all')
def list_courses():
    courses = Course.get_all_courses()
    return render_template('listCourses.html', courses=courses)

@course_bp.route('/courses/create', methods=['GET', 'POST'])
def create_course():
    if session.get('role') != 'instructor':
        flash('Permission denied. Only instructors can create courses.', 'error')
        return redirect('/afterlogin')
    
    if request.method == 'POST':
        course = Course.create_course(request.form, session['user_id'])
        flash(f'Course "{course.title}" created successfully!', 'success')
        return redirect('/courses/all')

    return render_template('create_course.html')

@course_bp.route('/courses/<int:course_id>/details')
def course_details(course_id):
    course = Course.get_by_id(course_id)
    if not course:
        flash('Course not found.', 'error')
        return redirect('/courses/all')

    is_enrolled = False
    if 'user_id' in session:
        is_enrolled = CourseEnrollment.query.filter_by(user_id=session['user_id'], course_id=course_id).first() is not None

    return render_template('courseDetails.html', course=course, is_enrolled=is_enrolled)

@course_bp.route('/courses/<int:course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    if 'user_id' not in session:
        flash('You must be logged in to enroll in a course.', 'error')
        return redirect('/login')
    
    is_success, message = CourseEnrollment.enroll_user(session['user_id'], course_id)
    if is_success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(f'/courses/{course_id}/enroll')

@course_bp.route('/my-courses')
def my_courses():
    if 'user_id' not in session:
        flash('Please log in to view your courses.', 'error')
        return redirect('/login')

    user = User.query.get(session['user_id'])
    enrolled_courses = [enrollment.course for enrollment in user.course_enrollments]

    return render_template('my_courses.html', enrolled_courses=enrolled_courses)


@course_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    if 'user_id' not in session:
        flash('You must be logged in to perform this action.', 'error')
        return redirect('/login')

    course = Course.get_by_id(course_id)
    if not course:
        flash('Course not found.', 'error')
        return redirect('/courses/all')

    if session.get('role') != 'admin' and session['user_id'] != course.instructor_id:
        flash('Permission denied. You are not authorized to delete this course.', 'error')
        return redirect('/courses/all')
    
    Course.delete_course(course_id)
    flash(f"Course '{course.title}' deleted successfully!", 'success')
    return redirect('/courses/all')