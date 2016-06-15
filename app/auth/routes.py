from flask import render_template, current_app, request, redirect, url_for, \
    flash, session
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForm
import bcrypt

from app.logic.user_management import UserManagment
from app import mongo
from app.models.user import User


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo["users"]
        existing_user = users.find_one({'name': request.form['username']})
        if existing_user is None:
            hass_pass = bcrypt.hashpw(request.form["passowrd"], bcrypt.gensalt())
            users.insert({
                'name': request.form['username'],
                'password': hass_pass
            })
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return "The username already exists!"
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
            and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserManagment.get_user_by_name(form.user_name.data)
        if user is None or not UserManagment.verify_password(user, form.password.data):
            flash('Invalid user name or password.')
            return redirect(url_for('.login'))
        login_user(User(user), form.remember_me.data, False)
        return redirect(request.args.get('next') or url_for('talks.index'))
    return render_template('auth/login.html', form=form)


@auth.route('/login2', methods=['POST'])
def login2():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        # check password
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) \
                == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('indexd'))
    return 'Invalid username or password'


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('talks.index'))
