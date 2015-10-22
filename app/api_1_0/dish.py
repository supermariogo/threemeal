# -*- coding:utf-8 -*-

from flask import jsonify
from . import api


@api.route('/dishes')
def get_dishes():
    return jsonify({'dish': 'test'})
