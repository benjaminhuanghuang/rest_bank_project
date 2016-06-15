class User():
    def __init__(self, user_data):
        self.data = user_data
        self.name = user_data["name"]
        self.password = user_data["password"]


    def is_active(self):
        return True

    def get_id(self):
        return str(self.data["_id"])





