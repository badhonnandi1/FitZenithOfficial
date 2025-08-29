from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        password = User.passwordEncryption(password)

        if not email or not password:
            flash('Email and password are required.', 'error')
            return redirect('/login')

        user = User.findUser(email)
        print(user)

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['role'] = user.role  

            return redirect('/afterlogin')
        else:
            flash('Invalid email or password.', 'error')
            return redirect('/login')
        
    return render_template("login_reg.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form.get('username')
        email = request.form.get('email')
        password = User.passwordEncryption(request.form.get('password'))

        if not all([name, email, password]):
            return "<h1>Error: All fields are required.</h1>"

        existing_user = User.findUser(email)
        if existing_user:
            flash('Email already registered. Please log in.', 'error')
            return redirect('/login')
        
        new_user = User(name=name, email=email, password=password)
        new_user.save()

        return redirect('/') 
        
    return render_template("login_reg.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')