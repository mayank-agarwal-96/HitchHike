import os
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from flask import g
# from HitchHike.welcome import get_db
from HitchHike.config import GOOGLE_API_KEY
from HitchHike.database import DataBase
from HitchHike.googleapi import GoogleApi

GOOGLE_DISTANCE = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&key={4}'

class AvailableCar(Document):
    
    doc_type = TextField(default='available_cars')
    owner = TextField()
    start = TextField()
    end = TextField()

    def save(self):
        db = DataBase.db()
        self.store(db)

    def update(self, origin, destination):
        db = DataBase.db()
        # car = AvailableCar.by_user(self.owner)
        self.start = origin
        self.end = destination

        self.store(db)        


    @classmethod
    def all(cls):
    	db = DataBase.db()
        return cls.view(db,'_design/cars/_view/all-cars/')

    @classmethod
    def by_user(cls,email):
        db = DataBase.db()
        cars = cls.view(
                        db,
                        '_design/cars/_view/by-user',
                        key=email,
                        include_docs=True
                        )
        if cars:
            result = []
            for c in cars:
                result.append(c)
            if len(result) > 0:
                return result[0]
            else:
                return None
        else:
        	return None


    @classmethod
    def delete(cls, user):
        db = DataBase.db()
        car = AvailableCar.by_user(user)
        if car:
            db.delete(car)            


class RequestRide(Document):
    doc_type = TextField(default='request_ride')
    postedby = TextField()
    origin = TextField()
    destination = TextField()
    acceptedby = TextField()
    accepted = BooleanField(default="False")

    def save(self):
        db = DataBase.db()
        self.store(db)


class Ride(Document):
    doc_type = TextField(default='ride')
    driver = TextField()
    hitchhiker = TextField()
    vehicle = TextField()
    fare = FloatField()
    distance = FloatField()
    origin = TextField()
    destination = TextField()
    driver_origin = TextField()
    driver_destination = TextField()


    def save(self):
        db = DataBase.db()
        self.store(db)

    @classmethod
    def by_user(cls,email):
        db = DataBase.db()
        rides = cls.view(
                        db,
                        '_design/ride/_view/ride-by-driver',
                        key=email,
                        include_docs=True
                        )
        if rides:
            result = []
            for c in rides:
                result.append(c)
            if len(result) > 0:
                return result[0]
            else:
                return None
        else:
            return None
    
    @classmethod
    def by_hitchhiker(cls,email):
        db = DataBase.db()
        rides = cls.view(
                        db,
                        '_design/ride/_view/ride-by-hitchhiker',
                        key=email,
                        include_docs=True
                        )
        if rides:
            result = []
            for c in rides:
                result.append(c)
            if len(result) > 0:
                return result[0]
            else:
                return None
        else:
            return None
    
    @classmethod
    def hitchhiker_history(cls, email):
        db = DataBase.db()
        rides = cls.view(
                        db,
                        '_design/ride/_view/hitch-previous-ride',
                        key=email,
                        include_docs=True
                        )

        if rides:
            result = []

            for i in rides:
                result.append(i)

            return result

        else:
            return None

    @classmethod
    def driver_history(cls, email):
        db = DataBase.db()
        rides = cls.view(
                        db,
                        '_design/ride/_view/driver-previous-ride',
                        key=email,
                        include_docs=True
                        )
        print rides
        if rides:
            result = []

            for i in rides:
                result.append(i)

            return result

        else:
            return None

    def calculate_distance(self):
        db = DataBase.db()
        self.distance = GoogleApi.distance(self.origin, self.destination)
        self.store(db)

    def calculate_fare(self):
        db = DataBase.db()
        self.fare =  float(self.distance/ 1000) * 4
        self.store(db)

    def stop(self):
        db = DataBase.db()
        self.doc_type = 'previous_ride'
        self.calculate_distance()
        self.calculate_fare()

        summary = {}
        summary['fare'] = self.fare
        summary['distance'] = self.distance
        self.store(db)
        return summary
