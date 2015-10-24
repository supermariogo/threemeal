# -*- coding:utf-8 -*-

import hashlib
import urllib

from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_security import UserMixin, RoleMixin
from flask_security.core import AnonymousUserMixin
from sqlalchemy.ext.associationproxy import association_proxy

from . import db, login_manager

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(60))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(36))
    about_me = db.Column(db.String(512))
    last_seen = db.Column(db.DateTime)

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    meals = db.relationship('Meal', backref="chef", lazy='dynamic')

    @property
    def password(self):
        # raise AttributeError('password is not a readable attribute')
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def __repr__(self):
        return '%s(%s)' % (self.nickname, self.email)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def get_gravatar_url(self):
        size = 40
        random = 'identicon'
        # construct the url
        gravatar_url = "http://www.gravatar.com/avatar/" + \
                       hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': random, 's': str(size)})
        return gravatar_url


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Meal(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    is_selected = db.Column(db.Boolean, default=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_date = db.Column(db.DateTime, default=db.func.now())
    zipcodes = association_proxy('meal_zipcodes', 'zipcodes')

    def __repr__(self):
        return '<Meal %r>' % self.name


class ZipCode(db.Model):
    __tablename__ = 'zipcode'
    id = db.Column(db.Integer(), primary_key=True)
    zip_code = db.Column(db.String(20))
    meals = association_proxy('meal_zipcodes', 'meals')

    def __repr__(self):
        return '<ZipCode %r>' % self.zip_code


class MealZipCode(db.Model):
    __tablename__ = 'meal_zipcode'
    meal_id = db.Column(db.Integer,
                        db.ForeignKey('meal.id'),
                        primary_key=True)
    zipcode_id = db.Column(db.Integer,
                           db.ForeignKey('zipcode.id'),
                           primary_key=True)
    begin_date = db.Column(db.Date, default=db.func.now())
    end_date = db.Column(db.Date, default=db.func.now())
    create_date = db.Column(db.DateTime, default=db.func.now())
    zipcodes = db.relationship(ZipCode,
                               backref=db.backref('meal_zipcodes',
                                                  cascade='all, delete-orphan')
                               )
    meals = db.relationship(Meal,
                            backref=db.backref('meal_zipcodes',
                                               cascade='all, delete-orphan'))
