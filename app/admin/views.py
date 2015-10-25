# -*- coding:utf-8 -*-

from flask import render_template, request, redirect, url_for
from .. import csrf
from ..decorators import superuser_required
from ..models import Meal
from . import admin


@admin.route('/')
def index():
    return 'hello admin!'


@csrf.exempt
@admin.route('/meals/<order_status>')
@superuser_required
def meals(order_status):
    """
    根据zipcode查找meals，并按照日期排序
    :param order_status: all, selected, unselected
    :return: the admin's meal list page
    """
    if order_status in ('selected', 'unselected'):
        selected = True if order_status=='selected' else False
        meals = Meal.query.filter_by(is_selected=selected).order_by(Meal.id.desc())
    else:
        order_status = 'all'
        meals = Meal.query.order_by(Meal.id.desc())
    return render_template('admin/meals.html', meals=meals)


@admin.route('/meal/<int:id>/edit')
@superuser_required
def meal_edit(id):
    """
    编辑meal，可以对meal进行推荐、取消推荐
    :param id: meal id
    :return: the admin's meal edit page
    """
    meal = Meal.query.get_or_404(id)
    selected = request.args.get('selected')
    if selected == 'yes':
        meal.is_selected = True
    elif selected == 'no':
        meal.is_selected = False
    return redirect(url_for('admin.meals', order_status='all'))


