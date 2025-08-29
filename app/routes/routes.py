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


@main_bp.route('/user/<int:user_id>/profile')
def view_user_profile(user_id):
    user = User.getUser(user_id)
    if not user:
        flash('Not found.', 'error')

    return render_template('profile.html', user=user)


@main_bp.route('/profile/edit')
def edit_profile():

    user = User().getUser(session.get('user_id'))
    return render_template('manageProfile.html', user=user)

@main_bp.route('/profile/update', methods=['GET', 'POST'])
def update_profile():
    user = User.getUser(session.get('user_id'))
    if not user:
        flash('User not found. Please log in again.', 'error')
        session.pop('user_id', None)
        return redirect(url_for('auth.login'))

    if request.method == 'POST':

        user.update(request.form)
        
        flash('Profile Updated', 'success')
        return redirect('profile/view')

    dob_formatted = user.dateOfBirth.strftime('%Y-%m-%d') if user.dateOfBirth else ''
    return render_template('manageProfile.html', user=user, dob_formatted=dob_formatted)