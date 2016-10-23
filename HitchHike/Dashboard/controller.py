import os

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user

dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/driver',methods=['GET'])
@login_required
def dash_driver():
    # if g.user:
        # print(GOOGLE_API_KEY)
    # print current_user.get_id()
    return render_template('dashdriver/index.html',map_key=GOOGLE_API_KEY)
    # return redirect(url_for('user.login'))

@dashboard.route('/hitchhiker',methods=['GET'])
@login_required
def dash_user():
    # if g.user:
        # print(GOOGLE_API_KEY)
    # print current_user.get_id()
    return render_template('dashhiker/index.html',map_key=GOOGLE_API_KEY)
    # return redirect(url_for('user.login'))


@dashboard.route('/profile')
@login_required
def profile():
	return render_template('dashboard/profile.html')
    # return redirect(url_for('user.login'))