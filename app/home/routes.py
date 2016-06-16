import os
from flask import render_template, current_app, request, redirect, url_for, flash, session, send_from_directory
from flask_login import login_user, logout_user, login_required
from . import home
from .forms import LoginForm
from app.models.user import User
from app import mongo


@home.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/image'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@home.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_name(form.user_name.data)
        if user and User.verify_password(user, form.password.data):
            user_obj = User(user)
            login_user(user_obj)

            # flash("Logged in successfully", category='success')
            return redirect(request.args.get('next') or url_for('statements.index'))
        else:
            flash('Invalid user name or password.', category='error')
    return render_template('home/index.html', form=form, title="Home")


@home.route('/mongotest')
def monog_test():
    users = [u for u in mongo.db.users.find()]

    return render_template('home/mongo_test.html', users=users)
