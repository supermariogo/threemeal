# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import client
from .forms import ClientOrderForm, MenuForm
from .. import db
from ..util import flash_errors
from ..models import Order, Meal, MealZipCode


@client.route('/', methods=['GET', 'POST'])
def index():
    form = MenuForm()
    if form.validate_on_submit():
        session['client_zipcode'] = form.zip_code.data
    return render_template('index.html', form=form)


@client.route('/client/order_meal/<int:id>', methods=['GET', 'POST'])
@login_required
def order_meal(id):
    meal = Meal.query.get_or_404(id)
    form = ClientOrderForm()
    zip = session.get('client_zipcode', '')
    zip_codes =(zip_code for zip_code in meal.zipcodes if zip_code.zip_code==zip)
    zip_code = None
    for zipcode in meal.zipcodes:
        if zipcode.zip_code == zip:
            zip_code = zipcode
            break
    else:
        flash_errors('error', u'该产品不支持您所在的区域')
        return redirect('/')
    if form.validate_on_submit():
        order = Order(meal_id=meal.id,
                      zipcode=zip_code,
                      client_id=current_user.id,
                      chef_id=meal.chef_id,
                      address=form.address.data,
                      phone=form.phone.data,
                      message=form.message.data,
                      status='UNHANDLED')
        db.session.add(order)
        db.session.commit()
    return render_template('client/order_meal.html', form=form, meal=meal)


@client.route('/client/order_detail/<int:id>')
@login_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    if not order.client_id == current_user.id:
        flash(u'你没有权限查看这个订单', message='error')
        return abort(403)
    return render_template('client/order_detail.html', order=order)


@client.route('/client/orders')
@login_required
def orders():
    return render_template('client/orders.html')


@client.route('/client/order_edit/<int:id>')
@login_required
def order_edit(id):
    return render_template('client/order_edit.html')
