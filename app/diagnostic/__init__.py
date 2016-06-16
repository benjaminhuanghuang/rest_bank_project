from flask import Blueprint

diagnostic = Blueprint('diagnostic', __name__)

from . import routes
