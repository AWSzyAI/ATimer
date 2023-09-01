#db.py

import sqlite3 # 导入sqlite3模块
import click # 导入click模块
from flask import current_app, g # 从flask模块导入current_app和g对象
from flask.cli import with_appcontext # 从flask.cli模块导入with_appcontext装饰器
from flask import current_app, g
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from .models import db
import os


# 获取数据库连接对象
def get_db():
    if 'db' not in g: # 如果g中没有db属性
        g.db = sqlite3.connect( # 创建数据库连接
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # 设置数据库连接的row_factory属性

    return g.db

# 关闭数据库连接
def close_db(e=None): 
  db = g.pop('db', None) # 从g中删除db属性

  if db is not None:
    db.close() # 关闭连接

# 初始化数据库
def init_db():
  db = get_db()

  # 执行schema.sql中的SQL语句
  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))

# 定义初始化数据库的命令行命令
@click.command('init-db')
@with_appcontext
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')

# 在app中注册数据库操作    
def init_app(app):
  # 注册teardown函数
  app.teardown_appcontext(close_db) 
  # 添加初始化数据库命令
  app.cli.add_command(init_db_command)