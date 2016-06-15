import os
from flask import render_template, current_app, send_from_directory

from . import home
from app import mongo


@home.route('/static/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/image'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@home.route('/')
def index():
    return render_template('home/index.html')


@home.route('/mongotest')
def monog_test():
    users = [u for u in mongo.db.users.find()]

    return render_template('home/mongo_test.html', users=users)
