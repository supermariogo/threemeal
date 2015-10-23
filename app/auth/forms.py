# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from ..models import User


class RegisterFrom(Form):
    nickname = StringField('nickname')
    email = EmailField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    def validate_email(self, field):
        email = field.data.strip()
        email = User.query.filter_by(email=email).first()
        if email:
            raise ValidationError(u'这个邮箱已经被注册过')

    def validate_password(self, field):
        password = field.data.strip()
        if len(password) < 3:
            raise ValidationError(u'密码长度不能小于3位')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')


class PasswordResetRequestForm(Form):
    """Reset password request form"""
    email = EmailField('Email', validators=[DataRequired()])


class PasswordResetForm(Form):
    """Reset password form"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')

    def validate_password(self, field):
        password = field.data.strip()
        if len(password) < 3:
            raise ValidationError('password must be 3 letter at least')