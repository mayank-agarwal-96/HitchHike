import os
import json
from .models import CarDriver, HitchHiker,User, Vehicle
from flask import Flask,Blueprint,session, redirect, flash, render_template, g, url_for, request
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from HitchHike.welcome import login_manager
from HitchHike.Dashboard.models import AvailableCar, Ride

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
        user.email = form_data.get('email',None)
        if user.email is None or user.email == "":
            flash("Email is required", category = "error")
        password = form_data.get('password',None)
        if password is None or password == "":
            flash("Password is required", category = "error") 
        user.set_password(password)
        user.phone = form_data.get('phoneno',None)
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
        user.email = form_data.get('email',None)
        if user.email is None or user.email == "":
            flash("Email is required", category = "error")
        password = form_data.get('password',None)
        if password is None or password == "":
            flash("Password is required", category = "error") 
        user.set_password(password)
        user.phone = form_data.get('phoneno',None)
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



@user.route('/hitchhiker/settings',methods=['GET', 'POST'])
@login_required
def hitchhiker_settings():
    user_id = current_user.get_id()
    user = HitchHiker.get_user(user_id)
    if user is not None:
        if request.method == 'POST':
            form_data = request.form
            print form_data
            name = form_data.get('name', None)
            email = form_data.get('email', None)
            phone = int(form_data.get('phone', None))
            password = form_data.get('password', None)

            user.update(name, phone, email, password)
            data = {}
            data['name'] = user.name
            data['email'] = user.email
            data['phone'] = user.phone
            return render_template('dashhiker/profile.html', data=data)

        else:
            data = {}
            data['name'] = user.name
            data['email'] = user.email
            data['phone'] = user.phone
            return render_template('dashhiker/profile.html', data=data)

    else:
        return "Forbidden : You are not allowed to view this page."
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
@user.route('/driver/settings',methods=['POST','GET'])
@login_required
def driver_setting():
    user_id=current_user.get_id()
    user =CarDriver.get_user(user_id)
    vehicle = Vehicle().get_by_user(user_id)
    type(user)
    data={}
    data['name']=user['name']
    data['phone']=user['phone']
    data['email']=user['email']
    data['carbrand']=vehicle['company']
    data['carmodel']=vehicle['model']
    data['carreg']=vehicle['reg_number']
    if user is None:
        return "Forbidden"
    if request.method == 'POST':
        form_data = request.form
        name = form_data.get('name',None)
        email = form_data.get('email',None)
        password = form_data.get('password',None)
        phone = form_data.get('phone',None)
        company = form_data.get('carbrand', None)
        model = form_data.get('carmodel', None)
        reg_number = form_data.get('carreg', None)
        user.update(name, phone, email, password)
        vehicle.update(company, reg_number, model)
        # return redirect(url_for('login'))
        return redirect(url_for('user.driver_setting'))
    return render_template('dashdriver/profile.html', data=data)
@user.route('/driver/ride/data',methods=['GET'])
@login_required
def driver_history_data():
    user_id=current_user.get_id()
    data=Ride.driver_history(user_id)
    rides =[]
    for i in data:
        rides.append(i._data)
    return json.dumps(rides)
@user.route('/driver/history',methods=['GET'])
@login_required
def driver_history():
    user_id=current_user.get_id()
    data=Ride.driver_history(user_id)
    return render_template('dashdriver/history.html', data=data)
@user.route('/hitchhiker/ride/data',methods=['GET'])
@login_required
def hitchhiker_history_data():
    user_id=current_user.get_id()
    data=Ride.hitchhiker_history(user_id)
    rides =[]
    for i in data:
        rides.append(i._data)
    return json.dumps(rides)
@user.route('/hitchhiker/history',methods=['GET'])
@login_required
def hitchhiker_history():
    user_id=current_user.get_id()
    data=Ride.hitchhiker_history(user_id)
    return render_template('dashhiker/history.html', data=data)

