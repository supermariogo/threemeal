# -*- coding:utf-8 -*-
from flask import flash


def flash_errors(form, dest='error'):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"%s 字段 - %s" % (
                getattr(form, field).label.text,
                error
            ), dest)