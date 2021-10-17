from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from werkzeug.security import check_password_hash
from blog.views import blog
from flask_login import LoginManager, login_user, logout_user
from models import User
from users.forms import RegisterForm, LoginForm
from datetime import datetime


users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Username address already exists')
            return render_template('register.html', form=form)
        new_user = User(username=form.username.data, password=form.password.data)

        db.session.add(new_user)
        db.session.commit()


        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again')

            return render_template("login.html", form=form)

        login_user(user)

        user.last_logged_in = user.current_logged_in
        user.current_logged_in = datetime.now()
        db.session.add(user)
        db.session.commit()
        return blog()
    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
