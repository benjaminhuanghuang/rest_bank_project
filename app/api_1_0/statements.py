from flask import jsonify, g
from app.logic.user_management import UserManagment

from . import api
from .errors import forbidden, bad_request

@api.route('/statements/list/<user_name>', methods=['GET'])
def list(user_name):
    if UserManagment.is_user_name_existed(user_name):
        return bad_request('User {} does not exist.'.format(user_name))

    if user_name != g.current_user.user_name:
        return forbidden('You cannot use this API.')


    return jsonify({'status': 'ok'})

@api.route('/statements/deposit', methods=['POST'])
def deposit():
    if not g.current_user.role > 0:
        return forbidden('You cannot use this API.')

    return jsonify({'status': 'ok'})


@api.route('/statements/withdraw', methods=['POST'])
def withdraw():
    if not g.current_user.role > 0:
        return forbidden('You cannot use this API.')
    return jsonify({'status': 'ok'})


@api.route('/admin/listuser', methods=['POST'])
def list_user():
    if not g.current_user.role > 0:
        return forbidden('You cannot use this API.')
    return jsonify({'status': 'ok'})
