#__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from . import db, views
import os

from dotenv import load_dotenv
load_dotenv()

from flask_migrate import Migrate

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',  # os.urandom(16)
        DATABASE=os.path.join(app.instance_path, 'ATimer.sqlite'),
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'ATimer.sqlite')


    from .models import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)


    from . import views
    app.register_blueprint(views.bp)
    app.add_url_rule('/', endpoint='index')

    migrate = Migrate(app, db)

    return app