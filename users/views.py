from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from werkzeug.security import check_password_hash
from blog.views import blog
from flask_login import LoginManager, login_user, logout_user
from models import User
from users.forms import RegisterForm, LoginForm
from datetime import datetime
import pyotp


users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username address already exists')
            return render_template('register.html', form=form)
        new_user = User(username=form.username.data, password=form.password.data, pinkey=form.pinkey.data)

        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():

    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')
            return render_template("login.html", form=form)
        if pyotp.TOTP(user.pinkey).verify(form.pinkey.data):

            # if user is verified reset login attempts to 0
            session['logins'] = 0

            login_user(user)

            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.add(user)
            db.session.commit()
        else:
            flash('You have to give valid 2fa!', 'danger')
        return blog()
    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
