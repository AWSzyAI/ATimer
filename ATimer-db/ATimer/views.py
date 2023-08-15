from flask import Blueprint, render_template, redirect, url_for,Flask

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
  return render_template('index.html',active_page='index')

@bp.route('/register')
def register():
    return render_template('register.html',active_page='register')

@bp.route('/login')
def login():
  return render_template('login.html',active_page='login')

@bp.route('/profile')
def profile():
  return render_template('profile.html',active_page='profile')

@bp.route('/create')  
def create():
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