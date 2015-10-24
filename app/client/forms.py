# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ClientOrderForm(Form):
    address = StringField('Address',
                          validators=[DataRequired(),
                                      Length(5, 256, message=u'地址在5-256个字符之间')
                                      ]
                          )
    phone = StringField('Phone',
                        validators=[DataRequired(message=u'请输入电话'),
                                    Length(5,20)])
    message = TextAreaField('Message',
                            validators=[Length(0, 256, message=u'不能超过256个字符')])
