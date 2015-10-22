# -*- coding:utf-8 -*-

from flask import Blueprint

cook = Blueprint('cook', __name__)

from . import views
