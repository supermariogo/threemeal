# -*- coding:utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import chef
from .forms import MealCreateForm


@chef.route('/')
@login_required
def index():
    return render_template('chef/chef_base.html')


@chef.route('/meal_list')
@login_required
def meal_list():
    """meal列表"""
    pass


@chef.route('/meal_create', methods=['GET', 'POST'])
@login_required
def meal_create():
    """创建meal"""
    form = MealCreateForm()
    if form.validate_on_submit():
        pass
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
