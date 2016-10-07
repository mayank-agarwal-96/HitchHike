import os

from .models import User
from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime


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

        db = g.db
        db[user.email] = user._data

        # return redirect(url_for('login'))
        return redirect(url_for('.login'))

    return render_template('signup.html')

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user', None)

        email = request.form['email']
       
        db = g.db
        user = db.get(email,None)
        if user is not None:
            if request.form['password'] == user['password']:
                session['user'] = user
                return redirect(url_for('.after_login'))

    return render_template('login.html')        



@user.route('/home')
def after_login():
    if g.user:
        return render_template('welcome.html')

    return redirect(url_for('.login'))