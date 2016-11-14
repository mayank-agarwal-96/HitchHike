import os
import json
import requests

from flask import Flask,Blueprint,session, redirect, render_template, g, url_for, request
from datetime import datetime
from HitchHike.config import GOOGLE_API_KEY
from flask_login import login_required, current_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from HitchHike.welcome import socketio

from HitchHike.User.models import CarDriver, HitchHiker, Vehicle
from .models import AvailableCar, Ride


dashboard=Blueprint("dashboard",__name__,template_folder="../template/dashboard",static_folder='../static')

GOOGLE_GEOCODE_URL = 'https://maps.googleapis.com/maps/api/geocode/json?place_id={0}&key={1}'

def reverse_geo_code(place_id):
    tu = (place_id, GOOGLE_API_KEY)
    location = requests.get(GOOGLE_GEOCODE_URL.format(*tu))
    lat = str(location.json()['results'][0]['geometry']['location']['lat'])
    lng = str(location.json()['results'][0]['geometry']['location']['lng'])

    return [lat, lng]


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
        # origin1 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?place_id='+i.start+'&key='+GOOGLE_API_KEY)
        # origin2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?place_id='+msg['orig']+'&key='+GOOGLE_API_KEY)
        # origin1lat = str(origin1.json()['results'][0]['geometry']['location']['lat'])
        # origin1lng = str(origin1.json()['results'][0]['geometry']['location']['lng'])
        # origin2lat = str(origin2.json()['results'][0]['geometry']['location']['lat'])
        # origin2lng = str(origin2.json()['results'][0]['geometry']['location']['lng'])
        origin1 = reverse_geo_code(i.start)
        origin2 = reverse_geo_code(msg['orig'])
        origin1lat = origin1[0]
        origin1lng = origin1[1]
        origin2lat = origin2[0]
        origin2lng = origin2[1]
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
@login_required
def accept_ride():
    data = json.loads(request.data)
    print data

    ride = Ride()
    ride.driver = data['owner']
    ride.hitchhiker = data['eid']
    ride.origin = data['orig']
    ride.destination = data['dest']
    ride.driver_origin = data['dorig']
    ride.driver_destination = data['ddest']
    ride.save()

    return json.dumps({'status':'OK'})


@dashboard.route('/driver/ride/', methods=['GET'])
@login_required
def driver_ride():
    user = current_user.get_id()
    if CarDriver.get_user(user):
        ride = Ride.by_user(user)
        print ride
        if ride is not None:
            data = {}
            hitch_origin_data = reverse_geo_code(ride.origin)
            hitch_dest_data = reverse_geo_code(ride.destination)
            driver_origin_data = reverse_geo_code(ride.driver_origin)
            driver_dest_data = reverse_geo_code(ride.driver_destination)
            data['hitch_orig_lat'] = hitch_origin_data[0]
            data['hitch_orig_lng'] = hitch_origin_data[1]
            data['hitch_dest_lat'] = hitch_dest_data[0]
            data['hitch_dest_lng'] = hitch_dest_data[1]
            data['driver_orig_lat'] = driver_origin_data[0]
            data['driver_orig_lng'] = driver_origin_data[1]
            data['driver_dest_lat'] = driver_dest_data[0]
            data['driver_dest_lng'] = driver_dest_data[1]
            return render_template('ride/driver.html', data = data,map_key=GOOGLE_API_KEY)

        else:
            return "No active rides currently."

    else:
        return "Error : Forbidden. \n You are not allowed to view this page."


@dashboard.route('/hitchhiker/ride/', methods=['GET'])
@login_required
def hitchhiker_ride():
    user = current_user.get_id()
    if HitchHiker.get_user(user):
        ride = Ride.by_hitchhiker(user)
        if ride is not None:
            return render_template('ride/hitchhiker.html')

        else:
            return "No active rides currently"    



@dashboard.route('/driver/ride/stop',methods=['GET', 'POST'])
def stop_ride():
    user = current_user.get_id()
    ride = Ride.by_user(user)
    if CarDriver.get_user(user):
        if ride:
            ride.doc_type = 'previous_ride'
            ride.calculate_distance()
            ride.calculate_fare()
            return "fare :" + str(ride.fare)

        else:
            return "No active ride"

    else:
        return "Forbidden"