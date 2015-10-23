# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User


@auth.route('/login')
def login():
    pass