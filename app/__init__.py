# -*- coding:utf-8 -*-

__author__ = 'Liu Lixiang'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)

    from .cook import cook as cook_blueprint
    app.register_blueprint(cook_blueprint, url_prefix='/cook')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app