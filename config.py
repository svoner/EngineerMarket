import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = os.path.abspath('app/static')
    ORDERS_PER_PAGE = 10
    ENGINEERS_PER_PAGE = 12
    HR_ENGINEERS_PER_PAGE = 20


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'P@ssw0rd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'P@ssw0rd'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
