from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from app import mongo

class UserManagment():
    @staticmethod
    def validate_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return UserManagment.get_user_by_id(id)
        return None

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def get_user_by_id(user_id):
        query = {"user_id": user_id}
        # projection = {"_id": -1}
        # user = mongo.db["users"].find_one(query, projection)
        user = mongo.db["users"].find_one(query)
        return user

    @staticmethod
    def get_user_by_name(user_name):
        query = {"name": user_name}
        # projection = {"_id": 0}
        # user = mongo.db["users"].find_one(query, projection)
        user = mongo.db["users"].find_one(query)
        return user

    @staticmethod
    def is_user_name_existed(user_name):
        query = {"name": user_name}
        count = mongo.db["users"].find(query).count()

        return count > 0

    @staticmethod
    def create_user(user_name, password, email, role=2):
        if UserManagment.is_user_name_existed(user_name):
            raise ValueError("User name {0} existed.".format(user_name))

        hass_pass = generate_password_hash(password)

        user = {
            "name": user_name,
            "password": hass_pass,
            "email": email,
            "role": role
        }

        mongo.db.users.insert(user)

    @staticmethod
    def verify_password(user, password):
        hash_pass = user["password"]
        return check_password_hash(hash_pass, password)
