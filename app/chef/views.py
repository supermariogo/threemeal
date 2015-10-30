# -*- coding:utf-8 -*-

from flask import render_template, redirect, url_for, abort, flash, request
from flask_login import login_required, current_user
from . import chef
from .forms import MealEditForm, ChefOrderEditForm, ChefApplyForm
from .. import db
from ..models import Meal, Zipcode, MealZipcode, Order, Role, ChefApply


@chef.before_app_first_request
def insert_chef_role():
    chef_role = Role.query.filter_by(name='chef').first()
    if not chef_role:
        Role.add(Role(name='chef'))


@chef.before_request
def before_request():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    if not current_user.has_role('chef') and \
                    request.endpoint != 'chef.chef_apply' and \
                    request.endpoint != 'chef.chef_apply_status':
        chefApply = ChefApply.query.filter_by(applicant_id=current_user.id) \
            .first()
        if chefApply:
            return redirect(url_for('chef.chef_apply_status', id=chefApply.id))
        return redirect(url_for('chef.chef_apply'))


@chef.route('/')
@login_required
def index():
    return render_template('chef/chef_base.html')


@chef.route('/apply', methods=['GET', 'POST'])
@login_required
def chef_apply():
    form = ChefApplyForm()
    if form.validate_on_submit():
        chefApply = ChefApply(applicant_id=current_user.id,
                              content=form.content.data,
                              status='waiting')
        db.session.add(chefApply)
        db.session.commit()
        return redirect(url_for('chef.chef_apply_status', id=chefApply.id))
    print('chef_apply')
    return render_template('chef/chef_apply.html', form=form)


@chef.route('/apply/<int:id>/status')
@login_required
def chef_apply_status(id):
    chefApply = ChefApply.query.get_or_404(id)
    if not (chefApply.applicant_id == current_user.id or
                current_user.has_role('admin')):
        abort(403)
    return render_template('chef/chef_apply_status.html', apply=chefApply)


@chef.route('/meal_list')
@login_required
def meal_list():
    """meal列表"""
    meals = Meal.query.filter_by(chef_id=current_user.id).order_by(Meal.id.desc())
    return render_template('chef/meal_list.html', meals=meals)


@chef.route('/meal_create', methods=['GET', 'POST'])
@login_required
def meal_create():
    """创建meal"""
    form = MealEditForm()
    if form.validate_on_submit():
        zipcodes = form.zipcodes.data
        meal = Meal(name=form.name.data,
                    description=form.description.data,
                    chef_id=current_user.id)
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
        return redirect(url_for('client.meal_detail', id=meal.id))
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
            meal_zipcode.begin_date = form.begin_date.data
            meal_zipcode.end_date = form.end_date.data
        zips = Zipcode.add_zips(form.zipcodes.data.split(','))
        while (len(meal.meal_zipcodes) > 0):
            meal.meal_zipcodes.pop()
        print(meal.meal_zipcodes)
        # create new MealZipcode
        for zipcode in zips:
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
    if len(meal.meal_zipcodes) > 0:
        form.begin_date.data = meal.meal_zipcodes[0].begin_date
        form.end_date.data = meal.meal_zipcodes[0].end_date
    return render_template('chef/meal_create.html', form=form)


@chef.route('/orders/<order_status>')
@login_required
def orders(order_status):
    """订单列表"""
    orders = Order.query.filter_by(chef_id=current_user.id).order_by(Order.id.desc())
    return render_template('chef/orders.html', orders=orders)


@chef.route('/order/<int:id>/detail', methods=['GET', 'POST'])
@login_required
def order_detail(id):
    """订单查看"""
    order = Order.query.get_or_404(id)
    if not (order.chef_id == current_user.id or current_user.has_role('superuser')):
        flash(u'你没有权限查看这个订单', category='error')
        return abort(403)
    return render_template('chef/order_detail.html', order=order)


@chef.route('/order/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def order_edit(id):
    """处理，已发货、未发货"""
    order = Order.query.get_or_404(id)
    if not (order.chef_id == current_user.id or current_user.has_role('superuser')):
        flash(u'你没有权限查看这个订单', category='error')
        return abort(403)
    form = ChefOrderEditForm()
    if form.validate_on_submit():
        order.status = form.status.data
        order.remark = form.remark.data
    form.status.data = order.status
    form.remark.data = order.remark
    return render_template('chef/order_edit.html', order=order, form=form)
