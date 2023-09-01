#models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.types import PickleType
from datetime import datetime, timedelta  # 用于处理日期和时间
from flask_sqlalchemy import SQLAlchemy  # 用于数据库操作
from werkzeug.security import generate_password_hash, check_password_hash  # 用于密码哈希



# 创建数据库实例
db = SQLAlchemy()

# 创建用户模型
class User(db.Model):
  __tablename__ = 'users'  # 数据库表名
  id = db.Column(db.Integer, primary_key=True)  # 用户ID，整数类型，主键
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
  id = db.Column(db.Integer, primary_key=True)  # 项目ID，整数类型，主键
  name = db.Column(db.String(64), nullable=False)  # 项目名称，字符串类型，不能为空
  status = db.Column(db.String(64), nullable=False)  # 项目状态，字符串类型，不能为空
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 项目所属用户ID，整数类型，外键，不能为空

  
  #description = db.Column(db.String(64), nullable=False)  # 项目描述，字符串类型，不能为空
  #start_time = db.Column(db.DateTime, nullable=False)  # 项目开始时间，日期时间类型，不能为空
  #end_time = db.Column(db.DateTime, nullable=False)  # 项目结束时间，日期时间类型，不能为空
  #duration = db.Column(db.Interval, nullable=False)  # 项目时长，时间间隔类型，不能为空

  #统计数据
  all_time = db.Column(db.Interval, nullable=False)  # 总时长，时间间隔类型，不能为空
  daily_time = db.Column(PickleType, nullable=False, default={})  # 日时长，字典类型，默认为空字典
  weekly_time = db.Column(PickleType, nullable=False, default={})  # 周时长，字典类型，默认为空字典
  monthly_time = db.Column(PickleType, nullable=False, default={})  # 月时长，字典类型，默认为空字典
  yearly_time = db.Column(PickleType, nullable=False, default={})  # 年时长，字典类型，默认为空字典

  #元数据
  records = db.relationship('Record', backref='records', lazy=True)  # 项目和记录之间的关联关系

  def update_duration(self):
      self.year = self.calculate_duration('year')  # 更新年时长
      self.month = self.calculate_duration('month')  # 更新月时长
      self.week = self.calculate_duration('week')  # 更新周时长
      self.day = self.calculate_duration('day')  # 更新日时长
      self.all = self.calculate_duration('all')  # 更新总时长

  def calculate_duration(self, duration_type):
      total_duration = timedelta()  # 初始化总时长为0秒
      for record in self.records:  # 遍历项目的记录
          if duration_type == 'year' or duration_type == 'all':
              total_duration += record.duration  # 累加记录的时长
          elif duration_type == 'month' and record.start_time.year == datetime.now().year:
              total_duration += record.duration  # 累加记录的时长（仅当记录发生在当前年份的某个月）
          elif duration_type == 'week' and record.start_time.strftime('%Y-%W') == datetime.now().strftime('%Y-%W'):
              total_duration += record.duration  # 累加记录的时长（仅当记录发生在当前年份的当前周）
          elif duration_type == 'day' and record.start_time.date() == datetime.now().date():
              total_duration += record.duration  # 累加记录的时长（仅当记录发生在当前日期）
      return total_duration
  
  def calculate_time(self):
    # 获取所有记录
    records = self.records 

    # 计算各维度时间    
    daily_time = {}
    weekly_time = {}
    monthly_time = {}
    yearly_time = {}

    for r in records:
      date = r.start_time.date()  
      day = date.strftime("%Y-%m-%d")
      week = date.strftime("%Y-W%W")
      month = date.strftime("%Y-%m")
      year = date.strftime("%Y")
      
      if day not in daily_time:
        daily_time[day] = timedelta()
      daily_time[day] += r.duration  

      if week not in weekly_time:
        weekly_time[week] = timedelta()
      weekly_time[week] += r.duration

      if month not in monthly_time:
        monthly_time[month] = timedelta()
      monthly_time[month] += r.duration
      
      if year not in yearly_time:
        yearly_time[year] = timedelta()
      yearly_time[year] += r.duration
    
    
    # 求总时间
    total_time = sum(daily_time.values()) 
    
    # 更新模型属性
    self.daily_time = daily_time
    self.weekly_time = weekly_time  
    self.monthly_time = monthly_time
    self.yearly_time = yearly_time
    self.total_time = total_time

    db.session.commit()

# 创建记录模型
class Record(db.Model):
  __tablename__ = 'records'  # 数据库表名
 
  id = db.Column(db.Integer, primary_key=True)  # 记录ID，整数类型，主键
  project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # 项目ID，整数类型，外键，不能为空
  start时间 = db.Column(db.DateTime, nullable=False)  # 记录开始时间，日期时间类型，不能为空
  end_time = db.Column(db.DateTime, nullable=False)  # 记录结束时间，日期时间类型，不能为空
  duration = db.Column(db.Interval, nullable=False)  # 记录时长，时间间隔类型，不能为空
  

  def __init__(self, start_time, end_time):
      self.start_time = start_time  # 初始化记录的开始时间
      self.end_time = end_time  # 初始化记录的结束时间
      self.duration = end_time - start_time  # 计算并设置记录的时长
      #self.project.update_time_stats() 

  def save(self):
      db.session.add(self)  # 将记录添加到数据库会话
      db.session.commit()  # 提交数据库会话
      #self.project.update_duration()  # 更新所属项目的时长信息
      db.session.commit()  # 再次提交数据库会话