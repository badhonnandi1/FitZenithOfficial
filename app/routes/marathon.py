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
        return redirect('/marathons/list')

    if request.method == 'POST':
        new_marathon, error = Marathon.create(request.form)
        if not error:
            flash(f'Marathon event "{new_marathon.title}" created successfully!', 'success')

        return redirect('/marathons/list')
    
    return render_template('create.html')

@marathon_bp.route('/<marathon_id>/delete', methods=['POST'])
def deleteMarathon(marathon_id):
    if session.get('role') != 'admin':
        return redirect('/marathons/list')

    marathon = Marathon.get_by_id(marathon_id)

    if marathon:
        Marathon.delete_by_id(marathon_id)
        flash(f"Marathon \"{marathon['title']}\" deleted successfully!", 'success')

    return redirect('/marathons/list')

@marathon_bp.route('/<marathon_id>')
def marathonDetails(marathon_id):

    marathon = Marathon.get_by_id(marathon_id)
    is_registered = False

    if 'user_id' in session:
        is_registered = MarathonRegistration.checkRegister(session['user_id'], marathon_id)
            
    return render_template('details.html', marathon=marathon, is_registered=is_registered)

@marathon_bp.route('/<marathon_id>/register', methods=['POST'])
def registerMarathon(marathon_id):


    user_id = session['user_id']
    flag, message = MarathonRegistration.register_user(user_id, marathon_id)
    
    if flag:
        flash(message, 'success')
    else:
        flash(message, 'error')
        
    return redirect(f'/{marathon_id}')
