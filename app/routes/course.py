from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.course import Course, CourseEnrollment
from app.models.user import User

course_bp = Blueprint('course', __name__)

@course_bp.route('/courses/all')
def list_courses():
    courses = Course.AllCourses()
    return render_template('listCourses.html', courses=courses)

@course_bp.route('/courses/create', methods=['GET', 'POST'])
def create_course():
    if request.method == 'POST':
        course = Course.createCourse(request.form, session['user_id'])
        flash(f'Course "{course.title}" created', 'success')
        return redirect('/courses/all')

    return render_template('createCourse.html')

@course_bp.route('/courses/<course_id>/details')
def course_details(course_id):
    course = Course.getCourseByID(course_id)
    if not course:
        flash('Painai', 'error')
        return redirect('/courses/all')

    result = False
    if 'user_id' in session:
        result = CourseEnrollment.is_enrolled(session['user_id'], course_id)

    return render_template('courseDetails.html', course=course, is_enrolled=result)

@course_bp.route('/courses/<course_id>/enroll', methods=['POST'])
def enroll_course(course_id):
    is_success, message = CourseEnrollment.enroll_user(session['user_id'], course_id)
    if is_success:
        flash(message, 'success')
    else:
        flash(message, 'error')
    
    return redirect(url_for('course.course_details', course_id=course_id))

@course_bp.route('/my-courses')
def my_courses():
    user = User.getUser(session['user_id'])
    enrolled_courses = [enrollment.course for enrollment in user.course_enrollments]

    return render_template('myCourses.html', enrolled_courses=enrolled_courses)


@course_bp.route('/courses/<id>/delete', methods=['POST'])
def delete_course(id):
    course = Course.getCourseByID(id)
    if not course:
        flash('Course not found.', 'error')
        return redirect('/courses/all')

    Course.deleteCourse(id)
    flash(f"Course '{course.title}' deleted successfully!", 'success')
    return redirect('/courses/all')