from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import request, current_app

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
    def verify_password(user_id, password):
        user = UserManagment.get_user_by_id(user_id)
        password_hash = user["password"]
        return check_password_hash(password_hash, password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def hash_password(self, password):
        return generate_password_hash(password)

    @staticmethod
    def get_user_by_id(user_id):
        query = {"user_id": user_id}
        projection = {"_id": -1}
        user = current_app.db.find_one(query, projection)

        return user

    @staticmethod
    def get_user_by_name(user_name):
        query = {"user_name": user_name}
        projection = {"_id": -1}
        user = current_app.db["users"].find_one(query, projection)

        return user

    @staticmethod
    def is_user_name_existed(user_name):
        query = {"user_name": user_name}
        count = current_app.db["users"].find(query).count()

        return count > 0

    @staticmethod
    def create_user(user_name, password, email, role):
        if UserManagment.is_user_name_existed(user_name):
            raise ValueError("User name {0} existed.".format(user_name))

        user = {
            "user_name": user_name,
            "password": password,
            "email": email,
            "role": role
        }
        current_app.db["users"].insert(user)
