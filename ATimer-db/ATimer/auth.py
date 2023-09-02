#auth.py

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .models import User, db


bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        #db = get_db()

        if User.query.filter_by(username=username).first():
            error = 'User {} already exists'.format(username)

        if not error:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            #return redirect(url_for('auth.login'))
        

        flash(error)
            
    return render_template('auth/register.html',active_page='register')

# 登录
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = User.query.filter_by(username=username).first()
      

        if not user or not user.check_password(password):
            error = 'Incorrect username or password'

        if not error:
            session['user_id'] = user.id
            return redirect(url_for('main.all'))

        flash(error)

    return render_template('auth/login.html',active_page='login')

# 个人资料
@bp.route('/profile')
def profile():
    return render_template('auth/profile.html',active_page='profile')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        

@bp.route('/logout')
def logout():
    session.clear() #session.pop('user_id', None)
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


