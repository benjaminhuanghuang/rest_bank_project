import unittest
from app import create_app, db
from app.logic.user_management import UserManagment

class UserManagement_TestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()


    def tearDown(self):
         self.app_context.pop()

    def test_create_user(self):
        user_name = "ut_test"
        UserManagment.create_user(user_name, "123", "ut_test@a.com", 2)

        user = UserManagment.get_user_by_name(user_name)

        self.assertIsNotNone(user)


