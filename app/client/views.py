# -*- coding:utf-8 -*-

from . import client


@client.route('/')
def index():
    return 'hello client!'
