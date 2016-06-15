import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # used for session
    SECRET_KEY = "*9527*"

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "ben.email.sender@gmail.com"
    MAIL_PASSWORD = "1@11@11@1"
    MAIL_DEFAULT_SENDER = 'Benjamin Huang'
    MAIL_FLUSH_INTERVAL = 3600  # one hour
    MAIL_ERROR_RECIPIENT = "benjaminhuanghuang@gmail.com,huang.huang@afficienta.com"

    # PyMongo understands the following configuration directives
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DBNAME = "rest_bank"
    MONGO_USERNAME = "admin"
    MONGO_PASSWORD = "abc123"
    # MONGO_URI = "mongodb://admin:abc123/localhost:27017/rest_bank"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    DB_SERVER_URI = "192.168.11.119:27017"
    DB_PASSWORD = "qxio90"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

