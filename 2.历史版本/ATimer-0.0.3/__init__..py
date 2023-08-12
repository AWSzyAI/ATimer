import os
from flask import Flask
from views import main

app = Flask(__name__)
app.register_blueprint(main)

@app.route('/')
def index():
    return 'Hello World!'