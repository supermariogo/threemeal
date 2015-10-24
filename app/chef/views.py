# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from . import chef
from .forms import MealCreateForm
from .. import db
from ..models import Meal, ZipCode, MealZipCode


@chef.route('/')
@login_required
def index():
    return render_template('chef/chef_base.html')


@chef.route('/meal_list')
@login_required
def meal_list():
    """meal列表"""
    pass


@chef.route('/meal_detail/<int:id>')
def meal_detail(id):
    """meal详情"""
    meal = Meal.query.get_or_404(id)
    return render_template('chef/meal_detail.html', meal=meal)


@chef.route('/meal_create', methods=['GET', 'POST'])
@login_required
def meal_create():
    """创建meal"""
    form = MealCreateForm()
    if form.validate_on_submit():
        zip_codes = form.zip_codes.data
        meal = Meal(name=form.name.data,
                    description=form.description.data,
                    chef=current_user._get_current_object())
        zips = ZipCode.add_zips(zip_codes.split(','))
        db.session.add(meal)
        db.session.commit()
        meal_zips = [MealZipCode(meal_id=meal.id,
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
    pass


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
