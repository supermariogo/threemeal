# -*- coding:utf-8 -*-

from . import cook


@cook.route('/')
def index():
    return 'hello chef!'

