import os
from . import home

from flask import send_from_directory, current_app


@home.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static/image'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')
