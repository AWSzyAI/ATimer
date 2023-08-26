from flask import Blueprint, render_template, redirect, url_for,Flask
from flask import request
from .models import User

bp = Blueprint('main', __name__)



@bp.route('/')
def index():
  users = User.query.all() # 查询所有用户
  return render_template('index.html',active_page='index',users=users)



@bp.route('/profile')
def profile():
  return render_template('profile.html',active_page='profile')


@bp.route('/create', methods=['GET', 'POST'])
def create():
  if request.method == 'POST':
    
    # 获取表单数据
    name = request.form['name']  
    status = request.form['status']

    # 创建项目逻辑

    return redirect(url_for('index'))

  return render_template('create.html',active_page='create')



@bp.route('/daily')
def daily():
    return render_template('daily.html',active_page='daily')

@bp.route('/weekly')
def weekly():
  return render_template('weekly.html',active_page='weekly') 

@bp.route('/monthly')
def monthly():
    return render_template('monthly.html',active_page='monthly')

@bp.route('/yearly')
def yearly():
    return render_template('yearly.html',active_page='yearly')


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp)
    
    return app