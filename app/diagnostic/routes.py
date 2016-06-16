from flask import render_template, request, redirect, url_for , current_app

from . import diagnostic

@diagnostic.route('/makecrash', methods=['POST'])
def makecrash():
    # when program crash here
    current_app.logger.error("Crashed in make_crash")
    return "aaaa"


@diagnostic.route('/index')
def index():
    return render_template('diagnostic/index.html')

