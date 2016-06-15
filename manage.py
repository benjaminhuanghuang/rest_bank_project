from app import create_app
from app.models.user import User
from flask_script import Manager, Server

app = create_app('default')
manager = Manager(app)
server = Server(port=9527)
manager.add_command("run", server)


@manager.command
def test():
    from subprocess import call
    call(['nosetests', '-v',
          '--with-coverage', '--cover-package=app', '--cover-branches',
          '--cover-erase', '--cover-html', '--cover-html-dir=cover'])


@manager.command
def adduser(user_name, email, role=2):
    """
        Register a new user.
        python manage.py adduser ben ben@gmail -r0
    """
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    User.create_user(user_name, password, email, role)

    print('User {0} was created successfully.'.format(user_name))


@manager.command
def hash_password(password):
    print User.hash_password(password)


if __name__ == '__main__':
    manager.run()
