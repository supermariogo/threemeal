# -*- coding:utf-8 -*-

from flask import render_template, request, redirect, url_for
from sqlalchemy.orm.util import join
from .. import csrf
from ..decorators import superuser_required
from ..models import Meal, MealZipcode, Zipcode
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
    order_status_dict = {'all': u'全部Meal', 'selected': u'推荐的Meal', 'unselected': u'其他Meal'}
    zipcode = request.args.get('zipcode')
    meals = Meal.query
    if order_status in ('selected', 'unselected'):
        selected = True if order_status=='selected' else False
        meals = meals.filter_by(is_selected=selected)
    if zipcode:
        zipcode = Zipcode.query.filter_by(zipcode=zipcode).first()
        if zipcode:
            #meals = meals.select_from(join(Meal, MealZipcode)).filter(MealZipcode.zipcode_id==zipcode.id)
            meals = meals.filter(Meal.id==MealZipcode.meal_id).filter(MealZipcode.zipcode_id==zipcode.id)
        else:
            meals = []
    return render_template('admin/meals.html', meals=meals,
                           order_status=order_status_dict[order_status],
                           zipcode=request.args.get('zipcode'))


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


