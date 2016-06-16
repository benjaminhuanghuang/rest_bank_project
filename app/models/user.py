from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import login_manager, mongo
from bson.objectid import ObjectId

class User():
    """
        For using Flask-Login, we need a user class that implements four methods:
        is_authenticated, is_active, is_anonymous and get_id.
        get_id() must return a unicode that uniquely identifies the user
        Flask-Login use user name (account name) as the identity of user
    """
    def __init__(self, user_data):
        '''

        '''
        self.user_data = user_data

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.user_data["_id"])

    def is_admin(self):
        return self.user_data["role"] < 1

    @property
    def username(self):
        return self.user_data["name"]

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def validate_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return User.get_user_by_id(id)
        return None

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    @staticmethod
    def get_user_by_id(user_id):
        query = {"_id": ObjectId(user_id)}
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
        if User.is_user_name_existed(user_name):
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





@login_manager.user_loader
def load_user(user_id):
    '''
    To be used load user object from session when access URL
    :param user_id:  Should be the same as user.get_id()
    '''
    user = User.get_user_by_id(user_id)
    if user:
        return User(user)
    return None