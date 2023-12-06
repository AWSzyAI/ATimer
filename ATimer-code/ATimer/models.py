#models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import PickleType
from datetime import datetime, timedelta  # 用于处理日期和时间
from flask_sqlalchemy import SQLAlchemy  # 用于数据库操作
from werkzeug.security import generate_password_hash, check_password_hash  # 用于密码哈希

from sqlalchemy.types import TypeDecorator, VARCHAR
import json



# 创建数据库实例
db = SQLAlchemy()


class JSONEncodedDict(TypeDecorator):
  """Represents an immutable structure as a json-encoded string."""
  impl = VARCHAR

  def process_bind_param(self, value, dialect):
    if value is not None:
      value = json.dumps(value)
    return value

  def process_result_value(self, value, dialect):
    if value is not None:
      value = json.loads(value)
    return value
  
def convert_duration(duration_str):
  hours, minutes, seconds = map(int, duration_str.split(':'))
  duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
  return duration

def str_time_to_seconds(time_str:str):
  """将时间字符串转换为秒数"""
  print(type(time_str))
  hours, minutes, seconds = map(int, time_str.split(':')) #分割HH:MM:SS
  seconds = hours * 3600 + minutes * 60 + seconds
  return seconds

def seconds_to_str_time(seconds):
  """将秒数转换为时间字符串"""
  hours = seconds // 3600
  minutes = seconds % 3600 // 60
  seconds = seconds % 60
  return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

def add_times(time1, time2):
  """将两个时间字符串相加,返回时间字符串"""
  seconds1 = str_time_to_seconds(time1)
  seconds2 = str_time_to_seconds(time2)
  seconds = seconds1 + seconds2
  res = seconds_to_str_time(seconds)
  return res 





# 创建用户模型
class User(db.Model):
  __tablename__ = 'users'  # 数据库表名
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 用户ID，整数类型，主键
  username = db.Column(db.String(64), unique=True, nullable=False)  # 用户名，字符串类型，唯一且不能为空
  password_hash = db.Column(db.String(128), nullable=False)  # 密码哈希值，字符串类型，不能为空
  
  # 用户和项目之间的关联关系
  # 一个 User 可以有多个相关的 Project,而一个 Project 只属于一个 User。
  #projects = db.relationship('Project', backref='User', lazy=True)  # 用户和项目之间的关联关系
  def __init__(self, username, password, id=None):
      self.username = username  # 初始化用户名
      self.set_password(password)  # 初始化密码
      self.id = id

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)  # 设置用户密码的哈希值

  def check_password(self, password):
      return check_password_hash(self.password_hash, password)  # 检查用户密码是否正确

# 创建项目模型
class Project(db.Model):
  __tablename__ = 'projects'  # 数据库表名
  
  #项目信息
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 项目ID，整数类型，主键
  name = db.Column(db.String(64), nullable=False)  # 项目名称，字符串类型，不能为空
  status = db.Column(db.String(64), default="Pause",nullable=False)  # 项目状态，字符串类型，不能为空
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 项目所属用户ID，整数类型，外键，不能为空
  
  #时间信息
  all_time = db.Column(db.String)
  daily_time = db.Column(JSONEncodedDict, default={}) 
  weekly_time = db.Column(JSONEncodedDict, default={})
  monthly_time = db.Column(JSONEncodedDict, default={})
  yearly_time = db.Column(JSONEncodedDict, default={})

  #根据user_id查询用户
  user = db.relationship('User', backref='projects', lazy=True)

  #元数据
  records = db.relationship('Record', backref='records', lazy=True)  # 项目和记录之间的关联关系

  def __init__(self, name, user_id, status, id=None):
    self.name = name  # 初始化项目名称
    self.user_id = user_id  # 初始化项目所属用户ID
    self.status = status
    self.id = id
    self.all_time = '00:00:00'
    self.daily_time = {}
    self.weekly_time = {}
    self.monthly_time = {}
    self.yearly_time = {}

    

  def update_time_stats(self,record):
    date = record.start_time.date()
    day = date.strftime("%Y-%m-%d")
    week = date.strftime("%Y-W%W")
    month = date.strftime("%Y-%m")
    year = date.strftime("%Y")

    duration = record.duration #String

    self.all_time = add_times(self.all_time,duration)

    if date.isoformat() in self.daily_time:
      
      self.daily_time[day] = add_times(self.daily_time[day],duration)
    else:
      self.daily_time[day] = duration

    if week in self.weekly_time:
      self.weekly_time[week] = add_times(self.weekly_time[week],duration)
    else:
      self.weekly_time[week] = duration
    
    if month in self.monthly_time:
      self.monthly_time[month] = add_times(self.monthly_time[month],duration)
    else:
      self.monthly_time[month] = duration

    if year in self.yearly_time:
      self.yearly_time[year] = add_times(self.yearly_time[year],duration)
    else:
      self.yearly_time[year] = duration

    db.session.commit()

# 创建记录模型
class Record(db.Model):
  __tablename__ = 'records'  # 数据库表名
 
  id = db.Column(db.Integer, primary_key=True,autoincrement=True)  # 记录ID，整数类型，主键
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # 项目ID，整数类型，外键，不能为空
  start_time = db.Column(db.DateTime, nullable=False)  # 记录开始时间，日期时间类型，不能为空
  end_time = db.Column(db.DateTime, nullable=False)  # 记录结束时间，日期时间类型，不能为空
  duration = db.Column(db.String, nullable=False, default='00:00:00')  # 记录时长，字符串类型，不能为空
  

  def __init__(self, start_time, end_time, project_id):
    self.start_time = start_time  # 初始化记录的开始时间
    self.end_time = end_time  # 初始化记录的结束时间
    # 计算并设置记录的时长，timedelta类型转换为字符串
    
    duration_seconds = (end_time - start_time).total_seconds()
    
    
    # 计算小时、分钟和秒数
    hours = int(duration_seconds // 3600)
    minutes = int((duration_seconds % 3600) // 60)
    seconds = int(duration_seconds % 60)

    # 格式化为HH:MM:SS字符串
    self.duration = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    self.project_id = project_id  # 初始化记录所属项目ID
    #self.project.update_time_stats() 

  def save(self):
    db.session.add(self)  # 将记录添加到数据库会话
    db.session.commit()  # 提交数据库会话
    #self.project.update_duration()  # 更新所属项目的时长信息
    db.session.commit()  # 再次提交数据库会话




