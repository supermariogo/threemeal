# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, abort
from flask_login import login_required, current_user
from . import chef
from .forms import MealEditForm
from .. import db
from ..models import Meal, Zipcode, MealZipcode


@chef.route('/')
@login_required
def index():
    return render_template('chef/chef_base.html')


@chef.route('/meal_list')
@login_required
def meal_list():
    """meal列表"""
    meals = Meal.query.filter_by(chef_id=current_user.id).order_by(Meal.id.desc())
    print(meals)
    return render_template('chef/meal_list.html', meals=meals)


@chef.route('/meal_detail/<int:id>')
def meal_detail(id):
    """meal详情"""
    meal = Meal.query.get_or_404(id)
    return render_template('chef/meal_detail.html', meal=meal)


@chef.route('/meal_create', methods=['GET', 'POST'])
@login_required
def meal_create():
    """创建meal"""
    form = MealEditForm()
    if form.validate_on_submit():
        zipcodes = form.zipcodes.data
        meal = Meal(name=form.name.data,
                    description=form.description.data,
                    chef=current_user._get_current_object())
        zips = Zipcode.add_zips(zipcodes.split(','))
        db.session.add(meal)
        db.session.commit()
        meal_zips = [MealZipcode(meal_id=meal.id,
                                 zipcode_id=zip.id,
                                 begin_date=form.begin_date.data,
                                 end_date=form.end_date.data)
                     for zip in zips]
        db.session.add_all(meal_zips)
        db.session.commit()
        return redirect(url_for('chef.meal_detail', id=meal.id))
    return render_template('chef/meal_create.html', form=form)


@chef.route('/meal_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def meal_edit(id):
    """编辑meal"""
    meal = Meal.query.get_or_404(id)
    if not current_user.has_role('superuser') and not meal.chef_id == current_user.id:
        abort(403)
    form = MealEditForm()
    if form.validate_on_submit():
        meal.name = form.name.data
        meal.description = form.description.data
        # update the begin and end date
        for meal_zipcode in meal.meal_zipcodes:
            meal_zipcode.begin_date=form.begin_date.data
            meal_zipcode.end_date = form.end_date.data
        zips = Zipcode.add_zips(form.zipcodes.data.split(','))
        # create new MealZipcode
        for zipcode in zips:
            if zipcode not in meal.zipcodes:
                meal_zipcode = MealZipcode(meal_id=meal.id,
                                           zipcode_id=zipcode.id,
                                           begin_date=form.begin_date.data,
                                           end_date=form.end_date.data)
                db.session.add(meal_zipcode)
        db.session.add(meal)
        db.session.commit()
    form.zipcodes.data = ','.join((zipcode.zipcode for zipcode in meal.zipcodes))
    form.name.data = meal.name
    form.description.data = meal.description
    form.begin_date.data = meal.meal_zipcodes[0].begin_date
    form.end_date.data = meal.meal_zipcodes[0].end_date
    return render_template('chef/meal_create.html', form=form)


@chef.route('/orders/<order_status>')
@login_required
def orders(order_status):
    """订单列表"""
    return render_template('chef/orders.html')


@chef.route('/order_details/<int:id>', methods=['GET', 'POST'])
@login_required
def order_details(id):
    """订单处理，已发货、未发货"""
    pass
