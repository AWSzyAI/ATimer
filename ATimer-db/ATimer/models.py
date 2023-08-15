from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
  # 用户模型定义
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True)
  password = db.Column(db.String(120))
  is_delete = db.Column(db.Boolean, default=False)
  is_active = db.Column(db.Boolean, default=True)
  create_time = db.Column(db.DateTime, default=datetime.now)
  update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class Project(db.Model):
  # 项目模型定义
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    remark = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

  

class Record(db.Model):
  # 记录模型定义
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    remark = db.Column(db.String(120))
    is_delete = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
