from flask import Blueprint, request, g
from app.models.user import User

api = Blueprint('api', __name__)

from . import errors, statements


@api.before_request
def before_api_request():
    if request.json is None:
        return errors.bad_request('Invalid JSON in body.')
    token = request.json.get('token')
    if not token:
        return errors.unauthorized('Authentication token not provided.')
    user = User.validate_auth_token(token)
    if not user:
        return errors.unauthorized('Invalid authentication token.')
    g.current_user = user
