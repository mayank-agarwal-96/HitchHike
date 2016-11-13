import os
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from flask import g
# from HitchHike.welcome import get_db
from HitchHike.database import DataBase

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
            return result[0]
        else:
        	return None


    @classmethod
    def delete(cls, user):
        db = DataBase.db()
        car = AvailableCar.by_user(user)
            
        db.delete(car)            


class RequestRide(Document):
    doc_type = TextField(default='request_ride')
    postedby = TextField()
    origin = TextField()
    destination = TextField()
    acceptedby = TextField()
    accepted = BooleanField(default="False")


class Ride(Document):
    doc_type = TextField(default='ride')
    driver = TextField()
    hitchhiker = TextField()
    vehicle = TextField()
    fare = FloatField()
    distance = FloatField()
    origin = TextField()
    destination = TextField()


    def save(self):
        db = DataBase.db()
        self.store(db)