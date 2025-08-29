from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.instructorApplication import InstructorApplication
from app.models.user import User

instructor_bp = Blueprint('instructor', __name__)

@instructor_bp.route('/apply', methods=['GET', 'POST'])
def apply_instructor():    
    user = User.getUser(session['user_id'])
    
    if request.method == 'POST':
        form_data = request.form
        InstructorApplication.create_application(user.id, form_data)
        flash('Your application has been submitted!', 'success')
        return redirect('/afterlogin')

    return render_template('applyInstructor.html', user=user)

@instructor_bp.route('/admin/applications')
def admin_applications():
    if session.get('role') != 'admin':
        return redirect('/')

    pending_applications = InstructorApplication.pendingApplication()
    return render_template('adminApplicationsView.html', applications=pending_applications)

@instructor_bp.route('/admin/applications/<int:app_id>/approve', methods=['POST'])
def approve_application(app_id):
    if session.get('role') != 'admin':
        return redirect('/')
    
    application = InstructorApplication.get_by_id(app_id)
    if application:
        application.approve()
        flash(f"Application from {application.name} approved.", 'success')
    else:
        flash('Application not found.', 'error')

    return redirect('/apply')

@instructor_bp.route('/admin/applications/<int:app_id>/disapprove', methods=['POST'])
def disapprove_application(app_id):
    if session.get('role') != 'admin':
        flash('Permission denied.', 'error')
        return redirect('/')
    
    application = InstructorApplication.get_by_id(app_id)
    if application:
        application.disapprove()
        flash(f"Application from {application.name} disapproved.", 'info')
    else:
        flash('Application not found.', 'error')
        
    return redirect('/apply')
