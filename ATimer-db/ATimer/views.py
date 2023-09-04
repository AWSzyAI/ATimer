#view.py

from flask import Blueprint, render_template, redirect, url_for,Flask,jsonify,session
from flask import request
from .models import User
from .models import Project
from .models import Record
from .models import db
from flask_login import login_required
from datetime import datetime, timedelta  # 用于处理日期和时间


bp = Blueprint('main', __name__)

@bp.route('/')
def index():
  users = User.query.all() # 查询所有用户
  return render_template('index.html',active_page='index',users=users)

@bp.route('/create', methods=['GET','POST']) 
def create():
  next_page = request.args.get('next')
  if request.method == 'POST':
    # 获取表单数据
    name = request.form['name']
    status = request.form['status']

    current_user = User.query.get(session['user_id'])
    
    # 创建项目
    project = Project(
      name=name, 
      status=status,
      user_id=current_user.id,
    )
    db.session.add(project)
    db.session.commit()

    if next_page:
      return redirect(url_for(next_page))
    
  return render_template('create.html',active_page='create')


def parse_datetime(datetime_str):
    # 解析日期时间字符串并返回 datetime 对象
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')

@bp.route('/create-record', methods=['POST'])
def create_record():
  # 获取表单数据
  data = request.get_json()

  project_id = data['project_id']
  print('获取到项目id:', project_id)

  
  start_time = data['start_time']
  print('获取到开始时间:', start_time)

  end_time = data['end_time']
  print('获取到结束时间:', end_time)

  
  record = Record(
    start_time=parse_datetime(start_time),
    end_time=parse_datetime(end_time),
    project_id=project_id
  )
  print('创建记录:', record)

  project = Project.query.get(project_id)
  print('获取到项目:', project)
  project.update_time_stats(record)
  print('更新项目时间统计信息')
  
  #db.session.add(record)
  #db.session.commit()

  return jsonify(status='success')



@login_required
@bp.route('/project/<int:id>/status', methods=['PUT'])
def change_project_status(id):

  project = Project.query.get(id)
  
  # 获取请求的新状态并更新
  project.status = request.form['status'] 
  db.session.commit()

  return jsonify(status='success')


# 项目详情
@bp.route('/all')
def all():
  projects = Project.query.order_by(Project.all_time.desc()).all()
  return render_template('views/all.html',active_page='all',projects=projects,next='all')

@bp.route('/daily')
def daily():
  projects = Project.query.order_by(Project.daily_time.desc()).all() 
  return render_template('views/daily.html', projects=projects,active_page='daily',next='daily')

@bp.route('/weekly')
def weekly():
  projects = Project.query.order_by(Project.weekly_time.desc()).all()
  return render_template('views/weekly.html',active_page='weekly',projects=projects,next='weekly')

@bp.route('/monthly')
def monthly():
  projects = Project.query.order_by(Project.monthly_time.desc()).all()  
  return render_template('views/monthly.html',active_page='monthly',projects=projects,next='monthly')

@bp.route('/yearly')
def yearly():
  projects = Project.query.order_by(Project.yearly_time.desc()).all()
  return render_template('views/yearly.html',active_page='yearly',projects=projects,next='yearly')


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp)
    
    return app