# -*- coding:utf-8 -*-

from . import chef


@chef.route('/')
def index():
    return 'hello chef!'


@chef.route('/publish_meal', methods=['GET', 'POST'])
def publish_meal():
    return "public meal"

