# -*- coding:utf-8 -*-

from datetime import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user
from sqlalchemy.orm.util import join
from .. import csrf, db
from ..decorators import superuser_required
from ..models import Meal, MealZipcode, Zipcode, ChefApply, Role, get_or_create
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
        selected = True if order_status == 'selected' else False
        meals = meals.filter_by(is_selected=selected)
    if zipcode:
        zipcode = Zipcode.query.filter_by(zipcode=zipcode).first()
        if zipcode:
            # meals = meals.select_from(join(Meal, MealZipcode)).filter(MealZipcode.zipcode_id==zipcode.id)
            meals = meals.filter(Meal.id == MealZipcode.meal_id).filter(MealZipcode.zipcode_id == zipcode.id)
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


@admin.route('/apply/list')
@superuser_required
def apply_list():
    apply_status_dict = {'all': u'全部Apply', 'approved': u'批准的Apply',
                         'waiting': u'待处理的Apply', 'refused': u'拒绝的Apply'}
    apply_status = request.args.get('apply_status')
    chefApplys = ChefApply.query
    if apply_status:
        apply_status_str = apply_status_dict[apply_status]
        if apply_status != 'all':
            chefApplys = chefApplys.filter(ChefApply.status == apply_status)
            print(chefApplys)
    else:
        apply_status = 'all'
        apply_status_str = apply_status_dict[apply_status]
    chefApplys = chefApplys.order_by(ChefApply.id.desc())
    return render_template('admin/apply_list.html', applys=chefApplys,
                           apply_status=apply_status,
                           apply_status_str=apply_status_str)


@admin.route('/apply/<int:id>/approve')
@superuser_required
def apply_approve(id):
    chefApply = ChefApply.query.get_or_404(id)
    chefApply.status = 'approved'
    chefApply.update_time = datetime.now()
    chefApply.admin = current_user
    chef_role = get_or_create(db.session, Role, name='chef')
    chefApply.applicant.roles.append(chef_role)
    db.session.add(chefApply.applicant)
    db.session.add(chefApply)
    db.session.commit()
    return redirect(url_for('chef.chef_apply_status', id=id))


@admin.route('/apply/<int:id>/refuse')
@superuser_required
def apply_refuse(id):
    chefApply = ChefApply.query.get_or_404(id)
    chefApply.status = 'refused'
    chefApply.update_time = datetime.now()
    chef_role = get_or_create(db.session, Role, name='chef')
    if chef_role in chefApply.applicant.roles:
        chefApply.applicant.roles.remove(chef_role)
    db.session.add(chefApply)
    db.session.commit()
    return redirect(url_for('chef.chef_apply_status', id=id))
