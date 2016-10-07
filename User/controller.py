
import os
import couchdb

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
user=Blueprint("user",__name__,template_folder="../template",static_folder='../static')
@user.route('/signup', methods=['GET', 'POST'])
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

	from database import Database
	database=Database()
        db = database.getDB()
        db[user.email] = user._data

        return redirect(url_for('login'))

    return render_template('signup.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        email = request.form['email']
       
	from database import Database
        database=Database()
        db = database.getDB()
        
        user = db.get(email,None)
        if user is not None:
            if request.form['password'] == user['password']:
                session['user'] = user
                return redirect(url_for('after_login'))
        # if request.form['password'] == 'password':
        #     session['user'] = request.form['email']
        #     return redirect(url_for('after_login'))

    return render_template('login.html')        


