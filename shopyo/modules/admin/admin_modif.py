"""
.. module:: AdminViews
   :synopsis: All endpoints of the admin views are defined here.

"""

from flask import (
    Blueprint, render_template, request, redirect

    )

from flask_login import login_required, current_user
from addon import db, login_manager

from project_api import base_context
from sqlalchemy import exists
from modules.admin.admin import admin_required
from modules.admin.models import Users

# Should maybe change URL?
admin_blueprint = Blueprint('admin', __name__,
                            template_folder='templates',
                            url_prefix='/admin'
                            )


@admin_blueprint.route("/")
@login_required
@admin_required
def user_list():
    """
           **Get The List of Users**

            Lists all users in the database.

    """
    context = base_context()
    context['users'] = Users.query.all()
    return render_template('admin/index.html', **context)


@admin_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def user_add():
    """
               **Adds a User**

            adds a user to database.

    """
    context = base_context()
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        password = request.form['password']
        admin_user = request.form.get('admin_user')
        if admin_user == 'True':
            admin_user = True
        else:
            admin_user = False

        has_user = db.session.query(exists().where(Users.id == id)).scalar()

        if has_user is False:
            new_user = Users(id=id, name=name, admin_user=admin_user)
            new_user.set_hash(password)
            db.session.add(new_user)
            db.session.commit()
            return render_template('admin/add.html', **context)
    return render_template('admin/add.html', **context)


@admin_blueprint.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_delete(id):
    """
                   **Delete a User**

        :param id: id of the user
        :type id: int

    """
    Users.query.filter(Users.id == id).delete()
    db.session.commit()
    return redirect('/admin')


@admin_blueprint.route('/edit/<id>', methods=['GET', 'POST'])
@login_required
@admin_required
def appointment_edit(id):
    """
                   **Update information for a User**

        :param id: id of the user
        :type id: int

    """
    context = base_context()
    u = Users.query.get(id)
    context['id'] = u.id
    context['name'] = u.name
    context['password'] = u.password
    context['admin_user'] = u.admin_user
    return render_template('admin/edit.html', **context)


@admin_blueprint.route('/update', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_update():
    """
                   **Update a User record**

    """
    id = request.form['id']
    name = request.form['name']
    password = request.form['password']
    admin_user = request.form.get('admin_user')
    if admin_user == 'True':
        admin_user = True
    else:
        admin_user = False
    u = Users.query.get(id)
    u.name = name
    u.set_hash(password)
    u.admin_user = admin_user
    db.session.add(u)
    db.session.commit()
    return redirect('/admin')
