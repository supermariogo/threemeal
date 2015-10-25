# -*- coding:utf-8 -*-

from flask import render_template, session, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from . import client
from .forms import ClientOrderForm, MenuForm, ClientOrderEditForm, ZipcodeForm
from .. import db
from ..util import flash_errors
from ..models import Order, Meal, MealZipcode, Zipcode


@client.route('/', methods=['GET', 'POST'])
def index():
    if 'client_zipcode' in session and Zipcode.is_valid(session['client_zipcode']):
        return redirect(url_for('client.menu', zipcode=session['client_zipcode']))
    else: # zipcode required
        form = ZipcodeForm()
        if form.validate_on_submit():
            session['client_zipcode'] = form.zipcode.data
            if Zipcode.is_valid(session['client_zipcode']):
                return redirect(url_for('client.menu', zipcode=session['client_zipcode']))
            else:
                flash('Invalid Zipcode', 'error')
        return render_template('index.html', form=form)


@client.route('/meal/<int:id>', methods=['GET', 'POST'])
def meal_detail(id):
    """meal详情"""
    meal = Meal.query.get_or_404(id)
    form = ClientOrderForm()
    client_zip = session.get('client_zipcode', '')
    show_modal = False
    for zipcode in meal.zipcodes:
        if zipcode.zipcode == client_zip:
            zipcode = zipcode
            break
    else:
        flash(u'该产品不支持您所在的区域', category='error')
        return redirect('/')
    if form.validate_on_submit():
        order = Order(meal_id=meal.id,
                      zipcode=zipcode,
                      client_id=current_user.id,
                      chef_id=meal.chef_id,
                      address=form.address.data,
                      phone=form.phone.data,
                      message=form.message.data,
                      status='UNHANDLED')
        db.session.add(order)
        db.session.commit()
        flash(u"下单成功", "info")
        return redirect(url_for('client.order_detail', id=order.id))
    elif request.method == 'POST':
        show_modal = True
    return render_template('client/meal_detail.html', meal=meal, form=form, show_modal=show_modal)


@client.route('/bechef', methods=['GET', 'POST'])
def bechef():
    return render_template('client/bechef.html')


@client.route('/menu/<zipcode>', methods=['GET', 'POST'])
def menu(zipcode):
    if Zipcode.is_valid(zipcode):
        zipcode = Zipcode.query.filter_by(zipcode=zipcode).first()
        if zipcode is None:
            return redirect(url_for('client.bechef'))
        meals = zipcode.meals
        return render_template('client/menu.html', meals=meals)
    else:
        flash('invaid zipcode')
        return redirect('/')


# @client.route('/order_meal/<int:id>', methods=['GET', 'POST'])
# def order_meal(id):
#     meal = Meal.query.get_or_404(id)
#     form = ClientOrderForm()
#     client_zip = session.get('client_zipcode', '')
#     for zipcode in meal.zipcodes:
#         if zipcode.zipcode == client_zip:
#             zipcode = zipcode
#             break
#     else:
#         flash(u'该产品不支持您所在的区域', category='error')
#         return redirect('/')
#     if form.validate_on_submit():
#         order = Order(meal_id=meal.id,
#                       zipcode=zipcode,
#                       client_id=current_user.id,
#                       chef_id=meal.chef_id,
#                       address=form.address.data,
#                       phone=form.phone.data,
#                       message=form.message.data,
#                       status='UNHANDLED')
#         db.session.add(order)
#         db.session.commit()
#         flash(u"下单成功", "info")
#         return redirect(url_for('client.order_detail', id=order.id))
#     return render_template('client/order_meal.html', form=form, meal=meal)


@client.route('/order_detail/<int:id>')
@login_required
def order_detail(id):
    order = Order.query.get_or_404(id)
    if not (order.client_id == current_user.id or current_user.has_role('superuser')):
        flash(u'你没有权限查看这个订单', category='error')
        return abort(403)
    return render_template('client/order_detail.html', order=order)


@client.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(client_id=current_user.id).order_by(Order.id.desc())
    return render_template('client/orders.html', orders=orders)


@client.route('/order_edit/<int:id>', methods=['GET', 'POST'])
@login_required
def order_edit(id):
    order = Order.query.get_or_404(id)
    if not (order.client_id == current_user.id or current_user.has_role('superuser')):
        flash(u'你没有权限编辑这个订单', category='error')
        return abort(403)
    form = ClientOrderEditForm()
    if form.validate_on_submit():
        if order.status == 'HANDLED' and form.status.data == 'CANCELED':
            flash(u'已经发货的订单不能取消')
            return redirect(url_for('client.order_edit', id=id))
        if order.status == 'UNHANDLED':
            order.address = form.address.data
            order.phone = form.phone.data
            order.message = form.message.data
    form.address.data = order.address
    form.phone.data = order.phone
    form.message.data = order.message
    #form.status.data = order.status
    return render_template('client/order_edit.html', form=form, order=order)
