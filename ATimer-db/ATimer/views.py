#view.py

from flask import Blueprint, render_template, redirect, url_for,Flask,jsonify
from flask import request
from .models import User
from .models import Project
from .models import Record
from .models import db

from flask_login import login_required



bp = Blueprint('main', __name__)



@bp.route('/')
def index():
  users = User.query.all() # 查询所有用户
  return render_template('index.html',active_page='index',users=users)



@bp.route('/profile')
def profile():
  return render_template('profile.html',active_page='profile')

@bp.route('/projects')
def projects():
  projects = Project.query.all()
  
  return render_template('projects.html', projects=projects)


@bp.route('/create', methods=['GET','POST']) 
def create():
  next_page = request.args.get('next')
  if request.method == 'POST':
    # 获取表单数据
    name = request.form['name']
    status = request.form['status']
    
    # 创建项目
    project = Project(name=name, status=status)
    db.session.add(project)
    db.session.commit()
    
    if next_page:
      return redirect(url_for(next_page))

  return render_template('create.html',active_page='create')

@login_required
@bp.route('/project/<int:id>/status', methods=['PUT'])
def change_project_status(id):

  project = Project.query.get(id)
  
  # 获取请求的新状态并更新
  project.status = request.form['status'] 
  db.session.commit()

  return jsonify(status='success')



@bp.route('/all')
def all():
    
    projects = Project.query.order_by(Project.all_time.desc()).all()
    return render_template('views/all.html',active_page='all',projects=projects)

@bp.route('/daily')
def daily():
    projects = Project.query.order_by(Project.day.desc()).all()
    return render_template('views/daily.html',active_page='daily',projects=projects,times=projects.day)

@bp.route('/weekly')
def weekly():
  return render_template('views/weekly.html',active_page='weekly') 

@bp.route('/monthly')
def monthly():
    return render_template('views/monthly.html',active_page='monthly')

@bp.route('/yearly')
def yearly():
    return render_template('views/yearly.html',active_page='yearly')


def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(bp)
    
    return app