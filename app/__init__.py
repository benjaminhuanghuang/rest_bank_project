from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pymongo import PyMongo

from flask_login import LoginManager
from config import config

bootstrap = Bootstrap()
moment = Moment()
mongo = PyMongo()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app(config_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        config_name: the python path of the config object in config.py,
    """
    app = Flask(__name__)
    config_obj = config[config_name]
    app.config.from_object(config_obj)

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # configure logging for production

        # email errors to the administrators
        if app.config.get('MAIL_ERROR_RECIPIENT') is not None:
            import logging
            from logging.handlers import SMTPHandler
            credentials = None
            secure = None
            if app.config.get('MAIL_USERNAME') is not None:
                credentials = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                if app.config['MAIL_USE_TLS'] is not None:
                    secure = ()

            # send log by email
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                toaddrs=[app.config['MAIL_ERROR_RECIPIENT']],
                subject='[Rest Bank] Application Error',
                credentials=credentials,
                secure=secure)

            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    mongo.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # register blue prints for routers
    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/1.0')

    from .statements import statements as statements_blueprint
    app.register_blueprint(statements_blueprint, url_prefix='/statements')

    return app
