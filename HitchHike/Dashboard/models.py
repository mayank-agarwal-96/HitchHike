import os
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from flask import g
from HitchHike.welcome import get_db

class AvailableCar(Document):
    
    doc_type = TextField(default='available_cars')
    owner = TextField()
    start = TextField()
    end = TextField()

    def save(self):
        db = g.db
        self.store(db)

    @classmethod
    def all(cls):
    	db = get_db()
        return cls.view(db,'_design/cars/_view/all-cars/')