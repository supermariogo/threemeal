#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db

app = create_app(os.getenv('THREEMEAL_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def add_admin():
    from app.models import Role, User
    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)
    db.session.commit()
    admin = User(nickname='admin',
                 email=app.config['THREEMEAL_ADMIN'],
                 password=app.config['THREEMEAL_ADMIN_PWD'])
    db.session.add(admin)
    db.session.commit()
    admin.roles = [user_role, super_user_role]
    db.session.add(admin)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
