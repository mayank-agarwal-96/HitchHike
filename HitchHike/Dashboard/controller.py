import os
import json
import requests

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user
from .models import AvailableCar
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from HitchHike.welcome import socketio
from HitchHike.User.models import CarDriver, HitchHiker, Vehicle
# from HitchHike.User.models import HitchHiker


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
    user = current_user.get_id()
    car = AvailableCar.by_user(user)
    if car is None:
        available = AvailableCar()
        available.owner = user
        available.start = data['orig']
        available.end = data['dest']
        available.save()
        return json.dumps({'status':'OK'})
    else:
        car.update(data['orig'], data['dest'])
        return json.dumps({'status':'OK'})

	    
@socketio.on('reqreceive')
def msgreceive(msg):
    print
    print "origin" , msg['orig']
    print "dest" , msg['dest']
    print
    msg['eid'] = session.get('user_id',None)
    # send(msg, broadcast=True)
    cars=AvailableCar.all();
    for i in cars:
        origin1 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?place_id='+i.start+'&key='+GOOGLE_API_KEY)
        origin2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?place_id='+msg['orig']+'&key='+GOOGLE_API_KEY)
        print 'https://maps.googleapis.com/maps/api/geocode/json?place_id='+i.start+'&key='+GOOGLE_API_KEY
        origin1lat = str(origin1.json()['results'][0]['geometry']['location']['lat'])
        origin1lng = str(origin1.json()['results'][0]['geometry']['location']['lng'])
        origin2lat = str(origin2.json()['results'][0]['geometry']['location']['lat'])
        origin2lng = str(origin2.json()['results'][0]['geometry']['location']['lng'])
        url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+origin1lat+','+origin1lng+'&destinations='+origin2lat+','+origin2lng+'&key='+GOOGLE_API_KEY
        print url
        dist = requests.get(url)
        print
        distval = dist.json()['rows'][0]['elements'][0]['distance']['value']
        print
        if ( distval <= 3000 ):
            msg['owner'] = i.owner
            emit('message', msg, room=i.owner)
    print

@socketio.on('messageaccept')
def msgaccept(msg):
    email = session.get('user_id',None)
    driver = CarDriver.get_user(email)
    print 'yolo'
    msg['deid'] = email
    msg['name'] = driver.name
    msg['phone'] = driver.phone
    vehicle = Vehicle.get_by_user(email)
    msg['vehicle'] = vehicle.company + " " + vehicle.model
    msg['regno'] = vehicle.reg_number
    print msg
    emit('message', msg, room=msg['eid'])

@socketio.on('joined')
def joined(message=None):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('user_id',None)    
    join_room(room)
    print
    # print "hurray in controller"
    print session.get('user_id')
    #emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)
    print
    print session
    print
    #print session.get('name') + ' has entered the room: ' + room


@dashboard.route('/driver/ride/accept',methods=['POST'])
def accept_ride():
    data = json.loads(request.data)
    print data
    return json.dumps({'status':'OK'})
