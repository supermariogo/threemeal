# -*- coding:utf-8 -*-

from flask import Blueprint

chef = Blueprint('chef', __name__)

from . import views
