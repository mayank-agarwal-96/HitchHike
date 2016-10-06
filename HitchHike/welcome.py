import os
import couchdb

from flask import Flask, session, redirect, render_template, g, url_for, request
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from User.controller import user
from config import cloudant_data

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(user,url_prefix="/user")

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db')

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

def get_db():
    if not hasattr(g, 'db'):
        server = couchdb.Server("https://"+cloudant_data['user']+':'+cloudant_data['password']+'@'+cloudant_data['host']+':'+cloudant_data['port'])
        with app.app_context():
            try:
                db = server.create('hitchhike')
            except:
                db = server['hitchhike']
    return db

@app.before_request
def before_request():
    g.db = get_db()
    g.user = None
    if 'user' in session:
        g.user = session['user']
