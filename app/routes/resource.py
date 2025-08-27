import os
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
from app.models.course import Course, CourseEnrollment
from app.models.resource import Resource
from app.models.user import User

resource_bp = Blueprint('resource', __name__)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resource_bp.route('/course/<int:course_id>/resources')
def list_resources(course_id):
    if 'user_id' not in session:
        flash('Please log in to view resources.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    is_enrolled = CourseEnrollment.is_enrolled(user_id, course_id)
    course = Course.get_by_id(course_id)
    
    is_instructor = course.instructor_id == user_id
    
    if not is_enrolled and not is_instructor and session.get('role') != 'admin':
        flash('You are not enrolled in this course.', 'error')
        return redirect(url_for('course.course_details', course_id=course_id))

    resources = Resource.get_by_course(course_id)
    return render_template('resources.html', resources=resources, course=course)


@resource_bp.route('/resource/upload/<int:course_id>', methods=['GET', 'POST'])
def upload_resource(course_id):
    if session.get('role') != 'instructor':
        flash('Only instructors can upload resources.', 'error')
        return redirect(url_for('course.course_details', course_id=course_id))

    course = Course.get_by_id(course_id)
    if course.instructor_id != session['user_id'] and session.get('role') != 'admin':
        flash('You are not the instructor of this course.', 'error')
        return redirect(url_for('course.course_details', course_id=course_id))
    
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        file = request.files['pdf_file']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            from uuid import uuid4
            filename = str(uuid4()) + "_" + secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads/resources')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            file_path = os.path.join(upload_folder, filename)
            
            file.save(file_path)

            Resource.create(
                title=request.form['title'],
                resource_number=request.form['resource_number'],
                course_id=course_id,
                instructor_id=session['user_id'],
                file_path=os.path.join('uploads/resources', filename)
            )

            flash('Resource uploaded successfully!', 'success')
            return redirect(url_for('resource.list_resources', course_id=course_id))
        else:
            flash('Invalid file type. Only PDFs are allowed.', 'error')
            return redirect(request.url)

    return render_template('upload_resource.html', course=course)

@resource_bp.route('/resource/delete/<int:resource_id>', methods=['POST'])
def delete_resource(resource_id):
    resource = Resource.get_by_id(resource_id)
    if session.get('role') != 'instructor' or resource.instructor_id != session['user_id'] and session.get('role') != 'admin':
        flash('You do not have permission to delete this resource.', 'error')
        return redirect(url_for('resource.list_resources', course_id=resource.course_id))
    
    try:
        os.remove(os.path.join(current_app.root_path, 'static', resource.file_path))
    except OSError as e:
        flash(f"Error deleting file: {e}", "error")

    Resource.delete(resource_id)
    flash('Resource deleted successfully.', 'success')
    return redirect(url_for('resource.list_resources', course_id=resource.course_id))

@resource_bp.route('/resource/view/<int:resource_id>')
def view_resource(resource_id):
    resource = Resource.get_by_id(resource_id)
    is_enrolled = CourseEnrollment.is_enrolled(session['user_id'], resource.course_id)
    is_instructor = resource.instructor_id == session['user_id']
    if not is_enrolled and not is_instructor and session.get('role') != 'admin':
        flash('You are not authorized to view this resource.', 'error')
        return redirect(url_for('course.course_details', course_id=resource.course_id))
        
    return render_template('view_resource.html', resource=resource)

@resource_bp.route('/resource/download/<int:resource_id>')
def download_resource(resource_id):
    resource = Resource.get_by_id(resource_id)
    is_enrolled = CourseEnrollment.is_enrolled(session['user_id'], resource.course_id)
    is_instructor = resource.instructor_id == session['user_id']
    if not is_enrolled and not is_instructor and session.get('role') != 'admin':
        flash('You are not authorized to download this resource.', 'error')
        return redirect(url_for('course.course_details', course_id=resource.course_id))
    
    return send_from_directory(os.path.join(current_app.root_path, 'static'), resource.file_path, as_attachment=True)