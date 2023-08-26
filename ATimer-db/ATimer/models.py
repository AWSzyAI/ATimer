from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

class User(db.Model):
  # 用户模型定义
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  password_hash = db.Column(db.String(128),nullable=True)

  def __init__(self, username, password_hash):
    self.username = username
    self.password_hash = password_hash
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  
class Project(db.Model):
  # 项目模型定义
  __tablename__ = 'projects'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True)
  status = db.Column(db.String(120))


  #remark = db.Column(db.String(120))
  #is_delete = db.Column(db.Boolean, default=False)
  #is_active = db.Column(db.Boolean, default=True)
  #create_time = db.Column(db.DateTime, default=datetime.now)
  #update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  

class Record(db.Model):
  # 记录模型定义
  __tablename__ = 'records'
  id = db.Column(db.Integer, primary_key=True)
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
  start_time = db.Column(db.DateTime, default=datetime.now)
  end_time = db.Column(db.DateTime, default=datetime.now)