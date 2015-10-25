# -*- coding:utf-8 -*-

from flask import render_template
from ..decorators import superuser_required
from . import admin


@admin.route('/')
def index():
    return 'hello admin!'


@admin.route('/meals/<order_status>')
@superuser_required
def meals(order_status):
    """
    根据zipcode查找meals，并按照日期排序
    :param order_status: all, selected, unselected
    :return: the admin's meal list page
    """
    return render_template('admin/meals.html')


@admin.route('/meal/<int:id>/edit')
@superuser_required
def meal_edit(id):
    """
    编辑meal，可以对meal进行推荐、取消推荐
    :param id: meal id
    :return: the admin's meal edit page
    """
    return render_template('admin/meal_edit.html')


