# -*- coding:utf-8 -*-

from flask import Blueprint

client = Blueprint('client', __name__)

from . import views

