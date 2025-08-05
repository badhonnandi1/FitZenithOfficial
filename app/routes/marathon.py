from turtle import title
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.marathon import Marathon, MarathonRegistration

marathon_bp = Blueprint('marathon', __name__)

@marathon_bp.route('/marathons/list')
def list_marathons():
    all_marathons = Marathon.get_all()
    return render_template('list.html', marathons=all_marathons)

@marathon_bp.route('/create', methods=['GET', 'POST'])
def createMarathon():
    if session.get('role') != 'admin':
        return redirect(url_for('marathon.list_marathons'))

    if request.method == 'POST':
        new_marathon, error = Marathon.create(request.form)
        if error:
            flash(f'Error creating event: {error}', 'error')
        else:
            flash(f'Marathon event "{new_marathon["title"]}" created successfully!', 'success')
        return redirect(url_for('marathon.list_marathons'))
    
    return render_template('create.html')

@marathon_bp.route('/<int:marathon_id>/delete', methods=['POST'])
def deleteMarathon(marathon_id):
    if session.get('role') != 'admin':
        flash('You do not have permission to delete marathons.', 'error')
        return redirect(url_for('marathon.list_marathons'))

    marathon = Marathon.get_by_id(marathon_id)

    if marathon:
        Marathon.delete_by_id(marathon_id)
        flash(f"Marathon \"{marathon['title']}\" deleted successfully!", 'success')

    return redirect(url_for('marathon.list_marathons'))

@marathon_bp.route('/<int:marathon_id>')
def marathonDetails(marathon_id):

    marathon = Marathon.get_by_id(marathon_id)
    is_registered = False

    if 'user_id' in session:
        is_registered = MarathonRegistration.checkRegister(session['user_id'], marathon_id)
            
    return render_template('details.html', marathon=marathon, is_registered=is_registered)

@marathon_bp.route('/<int:marathon_id>/register', methods=['POST'])
def register_for_marathon(marathon_id):

    if 'user_id' not in session:
        flash('You must be logged in to register.', 'error')
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    flag, message = MarathonRegistration.register_user(user_id, marathon_id)
    
    if flag:
        flash(message, 'success')
    else:
        flash(message, 'error')
        
    return redirect(url_for('marathon.marathonDetails', marathon_id=marathon_id))
