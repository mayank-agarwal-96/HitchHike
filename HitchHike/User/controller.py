import os

from .models import CarDriver, HitchHiker,User, Vehicle
from flask import Flask,Blueprint,session, redirect, flash, render_template, g, url_for, request
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from HitchHike.welcome import login_manager
from HitchHike.Dashboard.models import AvailableCar

user=Blueprint("user",__name__,template_folder="../template",static_folder='../static')

@login_manager.user_loader
def load_user(email):
    return User.get_user(email)

@user.route('/hitchhiker/signup', methods=['GET', 'POST'])
def hitchhikersignup():
    if request.method == "POST":

        form_data = request.form
        user = HitchHiker()

        user.name = form_data.get('name',None)
        if user.name is None or user.name == "":
            flash("Name is required", category = "error")
        user.username = form_data.get('username',None)
        if user.username is None or user.username == "":
            flash("Username is required", category = "error")
        user.email = form_data.get('email',None)
        if user.email is None or user.email == "":
            flash("Email is required", category = "error")
        password = form_data.get('password',None)
        if password is None or password == "":
            flash("Password is required", category = "error") 
        user.set_password(password)
        user.phone = form_data.get('phone',None)
        if user.phone is None:
            flash("Phone is required", category="error")
        # user.gender = form_data.get('gender',None)

        user.save()
        # return redirect(url_for('login'))
        return redirect(url_for('.login'))

    return render_template('signup.html')


@user.route('/signup', methods=['GET', 'POST'])
def cardriversignup():
    if request.method == "POST":

        form_data = request.form
        user = CarDriver()
        vehicle = Vehicle()

        user.name = form_data.get('name',None)
        if user.name is None or user.name == "":
            flash("Name is required", category = "error")
        user.username = form_data.get('username',None)
        if user.username is None or user.username == "":
            flash("Username is required", category = "error")
        user.email = form_data.get('email',None)
        if user.email is None or user.email == "":
            flash("Email is required", category = "error")
        password = form_data.get('password',None)
        if password is None or password == "":
            flash("Password is required", category = "error") 
        user.set_password(password)
        user.phone = form_data.get('phone',None)
        if user.phone is None:
            flash("Phone is required", category="error")

        vehicle.company = form_data.get('carcompany', None)
        if vehicle.company is None or vehicle.company == "" :
            flash("Vehicle company is required", category="error") 
        vehicle.model = form_data.get('vehicle', None)
        if vehicle.model is None or vehicle.model == "" :
            flash("Vehicle model is required", category="error")         
        vehicle.reg_number = form_data.get('regno', None)
        if vehicle.reg_number is None or vehicle.reg_number == "" :
            flash("Registration Number is required", category="error")         
        vehicle.owner = user.email
        user.save()
        vehicle.save()
        # return redirect(url_for('login'))
        return redirect(url_for('.login'))

    return render_template('signupcar.html')


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # session.pop('user', None)
        user = None
        if 'hitch-login' in request.form:
            email = request.form.get('HitchHikerEmail', None)
            # print email
            if email is not None:
                user = HitchHiker.get_user(email)
            # print user
            if user and user.check_password(request.form['hpassword']):
                login_user(user, remember=True)
                return redirect(url_for('dashboard.dash_user'))
            flash("Wrong username or password!", category='error')
            # return redirect(url_for('.login'))


        elif 'car-login' in request.form:
            email = request.form.get('CarDriverEmail', None)
            if email is not None:
                user = CarDriver.get_user(email)
                # print user.user_type
                if user and user.check_password(request.form['password']):
                    
                    login_user(user, remember=True)
                    return redirect(url_for('dashboard.dash_driver'))

                return redirect(url_for('.login'))
            return redirect(url_for('.login'))
 
    return render_template('login.html')        



@user.route('/update',methods=['PUT'])
def update():
    if request.method == 'PUT':
        pass

# @user.route('/home')
# def after_login():
#     if g.user:
#         return render_template('welcome.html')

#     return redirect(url_for('.login'))

@user.route('/logout')
@login_required
def logout():
    # session.pop('user', None)
    user = current_user.get_id()
    AvailableCar.delete(user)
    logout_user()
    return redirect(url_for('.login'))
