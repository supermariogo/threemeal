# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from ..models import Meal


class MealCreateForm(Form):
    zip_codes = StringField('Zip Code', validators=[DataRequired()])
    name = StringField('Meal Name', validators=[DataRequired()])
    description = TextAreaField()
