import os

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY

dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/',methods=['GET'])
def dashboardpage():
    print(GOOGLE_API_KEY)
    return render_template('dashboard/index.html',map_key=GOOGLE_API_KEY)


