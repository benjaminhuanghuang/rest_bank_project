from flask import render_template, flash, redirect, url_for, abort,\
    request, current_app
from flask_login import login_required, current_user

from . import statements

@statements.route('/')
@login_required
def index():

    return render_template('statements/list.html')