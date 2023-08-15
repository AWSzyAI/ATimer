from flask import Flask
from .models import db
from . import db, views
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    
    db.init_app(app)
    
    app.register_blueprint(views.main)

    return app