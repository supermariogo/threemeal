# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.fields.html5 import EmailField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from ..models import Meal


class MealEditForm(Form):
    zipcodes = StringField('Zip Code', validators=[DataRequired()])
    name = StringField('Meal Name', validators=[DataRequired()])
    description = TextAreaField()
    begin_date = DateField(u'Begin Date', validators=[DataRequired()])
    end_date = DateField(u'End Date', validators=[DataRequired()])


class ChefOrderEditForm(Form):
    status = SelectField('Status', coerce=unicode, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ChefOrderEditForm, self).__init__(*args, **kwargs)
        self.status.choices = [('HANDLED', u'发货'), ('CANCELED', u'取消订单')]
