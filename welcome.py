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


app = Flask(__name__)
app.secret_key = os.urandom(24)

cloudant_data = {
    'user' : 'c8f0887d-5214-4cd8-bb01-e7c0c8448c95-bluemix',
    'password' : "115a155b01dae21ffde4810f396f4e29166bc8e1b2472f667917fb6299938dad",
    'host' : 'c8f0887d-5214-4cd8-bb01-e7c0c8448c95-bluemix.cloudant.com',
    'port' : '443'
}

class User(Document):
    name = TextField()
    username = TextField()
    email = TextField()
    password = TextField()
    dob = DateTimeField(default = None)
    phone = IntegerField()
    gender = BooleanField()
    created = DateTimeField(default=datetime.now)
    category = TextField(default='User')


def get_db():
    if not hasattr(g, 'db'):
        server = couchdb.Server("https://"+cloudant_data['user']+':'+cloudant_data['password']
          +'@'+cloudant_data['host']+':'+cloudant_data['port'])

        try:
            g.db = server.create('hitchhike')
        except:
            g.db = server['hitchhike']        
    
    return g.db

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db')

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":

        form_data = request.form
        user = User()

        user.name = form_data.get('name',None)
        user.username = form_data.get('username',None)
        user.email = form_data.get('email',None)
        user.password = form_data.get('password',None)
        user.phone = form_data.get('phone',None)
        # user.gender = form_data.get('gender',None)

        db = get_db()
        db[user.email] = user._data

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        email = request.form['email']
        db = get_db()
        
        user = db.get(email,None)
        if user is not None:
            if request.form['password'] == user['password']:
                session['user'] = user
                return redirect(url_for('after_login'))
        # if request.form['password'] == 'password':
        #     session['user'] = request.form['email']
        #     return redirect(url_for('after_login'))

    return render_template('login.html')        

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
