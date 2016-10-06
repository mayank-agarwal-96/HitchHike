# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import couchdb

from flask import Flask, session, redirect, render_template, g, url_for, request
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from User.controller import user

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(user,url_prefix="/user")

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db')

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/home')
def after_login():
    if g.user:
        return render_template('welcome.html')

    return redirect(url_for('login'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
