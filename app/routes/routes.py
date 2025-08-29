from flask import Blueprint, render_template, request, redirect, url_for, flash,session, current_app
from app import db
from app.models.user import User
from app.models.announcement import Announcement
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def landing_page():
    return render_template('index.html')

@main_bp.route('/afterlogin')
def afterlogin_page():
    return render_template('afterindex.html')


@main_bp.route('/profile/view')
def view_profile():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session.get('user_id')
    return redirect('/user/{}/profile'.format(user_id))


@main_bp.route('/user/<user_id>/profile')
def view_user_profile(user_id):
    user = User.getUser(user_id)
    if not user:
        flash('Not found.', 'error')

    return render_template('profile.html', user=user)


@main_bp.route('/profile/edit')
def edit_profile():

    user = User().getUser(session.get('user_id'))
    return render_template('manageProfile.html', user=user)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@main_bp.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    user = User.getUser(session.get('user_id'))
    if not user:
        flash('User not found. Please log in again.', 'error')
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        
        file = request.files.get('profile_pic')
        new_filename = None
        
        if file and file.filename != '' and allowed_file(file.filename):
            from uuid import uuid4
            filename = str(uuid4()) + "_" + secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, 'static/uploads/profile_pics')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            new_filename = os.path.join('uploads/profile_pics', filename)

        user.update(request.form, new_filename)
        
        flash('Profile Updated', 'success')
        return redirect(url_for('main.view_profile'))

    dob_formatted = user.dateOfBirth.strftime('%Y-%m-%d') if user.dateOfBirth else ''
    return render_template('manageProfile.html', user=user, dob_formatted=dob_formatted)