from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from . import db
from .forms import RegisterForm, LoginForm


# registers auth blueprint
auth_bp = Blueprint('auth', __name__)

# register route -
@auth_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()
            # checks the user already registered
            if existing_user:
                flash('Username already taken', 'danger')
                return redirect(url_for('auth.register'))
            try:
                # add new user to the db
                new_user = User(username=form.username.data)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful. Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred during registration. Please try again.', 'danger')
                return render_template('register.html', form=form)
    return render_template('register.html', form=form)

# login route -
@auth_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            # check username and password to login
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Login Successful', 'success')
                return redirect(url_for('main.index'))  
            else:
                flash('Invalid username or password', 'danger')
                return redirect(url_for('auth.login'))
    return render_template('login.html', form=form)

# logout route -
@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'Goodbye {username}! See you again', 'info')
    return redirect(url_for('auth.login', username=username))
