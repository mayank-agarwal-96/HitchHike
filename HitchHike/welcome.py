import os
import couchdb
# import eventlet

from flask import Flask, session, redirect, render_template, g, url_for, request
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from config import cloudant_data
from flask_login import LoginManager
# from flask_socketio import SocketIO, send

# eventlet.monkey_patch()
app = Flask(__name__)
app.secret_key = os.urandom(24)
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'
# socketio = SocketIO(app, async_mode='eventlet')
# socketio.init_app(app)

@app.route('/')
def Welcome():
    return redirect(url_for('user.login'))
    # return app.send_static_file('index.html')

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
    
    # g.user = None
    # if 'user' in session:
    #     g.user = session['user']

from User.controller import user    # To prevent circular imports
from Dashboard.controller import dashboard
app.register_blueprint(user,url_prefix="/user")
app.register_blueprint(dashboard,url_prefix="/dashboard")