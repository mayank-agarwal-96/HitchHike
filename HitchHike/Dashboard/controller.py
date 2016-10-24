import os

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from HitchHike.welcome import socketio

dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/driver',methods=['GET'])
@login_required
def dash_driver():
    # user_id = current_user.get_id()
    return render_template('dashdriver/index.html',map_key=GOOGLE_API_KEY)

@dashboard.route('/hitchhiker',methods=['GET'])
@login_required
def dash_user():
# user_id = current_user.get_id()
    return render_template('dashhiker/index.html',map_key=GOOGLE_API_KEY)


@dashboard.route('/profile')
@login_required
def profile():
	return render_template('dashboard/profile.html')
    # return redirect(url_for('user.login'))

# clients = {}
@socketio.on('search')
def join(location):
    room = 'room_cars'
    # username = current_user.get_id()
    print
    print "location" , location
    print
    # location['sid'] = request.sid
    # clients[username] = location
    # print clients
    join_room(room)
    send(location, room=room)

    # clients.append(request.sid)