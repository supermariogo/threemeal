# -*- coding:utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import client
from .forms import ClientOrderForm
from ..models import Order, Meal, MealZipCode


@client.route('/')
def index():
    return render_template('index.html')


@client.route('/client/order_meal/<int:id>', methods=['GET', 'POST'])
@login_required
def order_meal(id):
    meal = Meal.query.get_or_404(id)
    form = ClientOrderForm()
    if form.validate_on_submit():
        pass
    return render_template('client/order_meal.html', form=form, meal=meal)