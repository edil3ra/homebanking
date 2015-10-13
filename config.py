import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    
    @staticmethod
    def init_app(app):
        pass
    

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_BOOK_DEV') or\
                              'sqlite:///{}'.format(os.path.join(basedir, 'data-dev.sqlite'))
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    def init_app(app):
        app.debug = True


class TestConfig(Config):
    TEST = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_BOOK_TEST') or\
                              'sqlite:///{}'.format(os.path.join(basedir, 'data-test.sqlite'))


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI_BOOK') or\
                              'sqlite:///{}'.format(os.path.join(basedir, 'data.sqlite'))


config = {
    'development': DevelopmentConfig,
    'test': TestConfig,
    'prod': ProdConfig,
    'default': DevelopmentConfig
}
