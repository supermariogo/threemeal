# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you never guess'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SUBJECT_PREFIX = '[Three Meal]'
    MAIL_SENDER = 'Three Meal Admin<admin@threemeal.com>'
    THREEMEAL_ADMIN = os.environ.get('THREEMEAL_ADMIN') or '550488300@qq.com'
    THREEMEAL_ADMIN_PWD = os.environ.get('THREEMEAL_ADMIN_PWD') or '123456'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    # s3 max file size
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max
    ALLOWED_EXTENSIONS = set(['txt', 'doc', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'data-TEST.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'data-TEST.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
