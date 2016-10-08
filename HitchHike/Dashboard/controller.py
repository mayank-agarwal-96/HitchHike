import os

from User.models import User
from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from config import GOOGLE_API_KEY

dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/',methods=['GET'])
def dashboard():

    return render_tempate('index.html',map_key=GOOGLE_API_KEY)


