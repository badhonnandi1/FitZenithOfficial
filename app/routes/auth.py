from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        password = User.passwordEncryption(password)

        if not email or not password:
            return "<h1>Error: Email and password are required.</h1>"

        user = User.findUser(email)

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['role'] = user.role  

            return redirect(url_for('main.afterlogin_page'))
        else:
            return "<h1>Login Failed. Check your email and password.</h1>"

    return render_template("login_reg.html")

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration"""
    if request.method == 'POST':

        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([name, email, password]):
            return "<h1>Error: All fields are required.</h1>"

        existing_user = User.findUser(email)
        if existing_user:
            return "<h1>Error: A user with that email already exists.</h1>"

        new_user = User(name=name, email=email, password=password)
        new_user.save()

        return redirect(url_for('main.landing_page')) 
        
    return render_template("login_reg.html")

@auth_bp.route('/logout')
def logout():
    """Logout page route"""
    return render_template('index.html')