import os
import json

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user
from .models import AvailableCar
# from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
# from HitchHike.welcome import socketio


dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

@dashboard.route('/driver',methods=['GET'])
@login_required
def dash_driver():
    return render_template('dashdriver/index.html',map_key=GOOGLE_API_KEY)
    # else:
    # 	return redirect(url_for('user.login'))

@dashboard.route('/hitchhiker',methods=['GET'])
@login_required
def dash_user():
    return render_template('dashhiker/index.html',map_key=GOOGLE_API_KEY)

@dashboard.route('/profile')
@login_required
def profile():
	return render_template('dashboard/profile.html')
    # return redirect(url_for('user.login'))

@dashboard.route('/postride/', methods=['POST'])
@login_required
def post_ride():
    # print "inPOST"
    data = json.loads(request.data)
    # print data
    available = AvailableCar()
    available.user = current_user.get_id()
    available.start = data['orig']
    available.end = data['dest']
    available.save()
    return json.dumps({'status':'OK'})
	    
#@socketio.on('message')
#def join(msg):
#    #room = 'room_cars'
#    # username = current_user.get_id()
#    print
#    print "origin" , msg
#    print
#    # location['sid'] = request.sid
#    # clients[username] = location
#    # print clients
#    #join_room(room)
#    send(msg, broadcast=True)
#
#    # clients.append(request.sid)
#
#
# @socketio.on('joined')
# def join(message=None):
#     """Sent by clients when they enter a room.
#     A status message is broadcast to all people in the room."""
#     room = "prafful"#session.get('user_id',None)    
#     join_room(room)
#     #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
#     print "helllloooooooooo"
#     print rooms['']['prafful']