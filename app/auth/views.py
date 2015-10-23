# -*- coding:utf-8 -*-
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, \
    current_user

from . import auth
from .. import db
from ..models import User
from ..email import send_email
from ..util import flash_errors
from .forms import RegisterFrom, LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.data['email']
        remember_me = form.data['remember_me']
        user = User.query.filter_by(email=email).first()
        if user is None:  # also enable user name login
            user = User.query.filter_by(nickname=email).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=remember_me)
            flash(u"登录成功", 'info')
            next = request.args.get('next') or '/'
            return redirect(next)
        else:
            flash(u'邮箱或者密码错误', 'login_form_error')
    else:
        flash_errors(form, 'login_form_error')
    return render_template('auth/login.html', form=form, current_user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterFrom()
    if request.method == 'POST':
        if form.validate_on_submit():
            u = User(nickname=form.data['nickname'],
                     email=form.data['email'],
                     password=form.data['password'])
            db.session.add(u)
            db.session.commit()

            send_email(u.email, u'欢迎加入每日三餐', 'email/welcome', user=u)
            flash(u'注册成功', 'info')
            login_user(u)
            return redirect(url_for('client.index'))
        else:
            flash_errors(form, "register_form_error")
    return render_template('auth/signup.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("logout successfully", "info")
    return redirect("/")