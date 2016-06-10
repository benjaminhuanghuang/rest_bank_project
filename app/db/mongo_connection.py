from pymongo import MongoClient


class MongoConnection(object):
    @staticmethod
    def init_db(app):
        try:
            conn = MongoClient(app.config['DB_SEVER_URI'], app.config['DB_SEVER_PORT'])
            db_conn = conn[app.config['DATABASE']]
            db_conn.authenticate(app.config['DB_USER'], app.config['DB_PASSWORD'])
            return db_conn
        except Exception as e:
            app.logger.error("Can not connect to database {}:{} as user {}. {}"
                             .format(app.config['DB_SEVER_URI'], app.config['DB_SEVER_URI'],
                                     app.config['DB_USER'], e.message))
