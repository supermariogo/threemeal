# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class ZipcodeForm(Form):
    zipcode = StringField('zipcode',
                          validators=[DataRequired(),
                                      Length(1, 10, message=u'zipcode在1-10个字符之间')
                                      ]
                          )

class MenuForm(Form):
    zip_code = StringField('Address',
                          validators=[DataRequired(),
                                      Length(1, 10, message=u'地址在1-10个字符之间')
                                      ]
                          )


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


class ClientOrderEditForm(ClientOrderForm):
    status = SelectField('Status', coerce=unicode, validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(ClientOrderEditForm, self).__init__(*args, **kwargs)
        self.status.choices = [('COMPLETED', u'完成'), ('CANCELED', u'取消订单')]

