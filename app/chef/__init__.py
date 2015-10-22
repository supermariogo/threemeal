# -*- coding:utf-8 -*-

from flask import Blueprint

cook = Blueprint('chef', __name__)

from . import views
