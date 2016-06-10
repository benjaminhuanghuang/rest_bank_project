from app import create_app
from app.logic.user_management import UserManagment
from flask_script import Manager

app = create_app('default')
manager = Manager(app)


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def adduser(user_name, email):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    UserManagment.create_user(user_name, password, email, 2)


    print('User {0} was created successfully.'.format(user_name))


if __name__ == '__main__':
    manager.run()

