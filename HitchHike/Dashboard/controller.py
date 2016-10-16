import os

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user

dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/',methods=['GET'])
@login_required
def dashboardpage():
    # if g.user:
        # print(GOOGLE_API_KEY)
    print current_user.get_id()
    return render_template('dashboard/index.html',map_key=GOOGLE_API_KEY)
    # return redirect(url_for('user.login'))

@dashboard.route('/profile')
@login_required
def profile():
	return render_template('dashboard/profile.html')
    # return redirect(url_for('user.login'))