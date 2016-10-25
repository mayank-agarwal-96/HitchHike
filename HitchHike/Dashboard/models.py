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
        db = get_db()
        self.store(db)

    @classmethod
    def all(cls):
    	db = get_db()
        return cls.view(db,'_design/cars/_view/all-cars/')

    # @classmethod
    # def by_user(cls,email):
    #     db = get_db()
    #     cars = cls.view(
    #                     db,
    #                     '_design/cars/_view/by-user',
    #                     key=email,
    #                     include_docs=True
    #                     )
    #     if cars:
    #         result = []
    #         for c in cars:
    #             result.append(cls.wrap(c))
    #         result result[0]
    #     else:
    #     	return None

    @classmethod
    def delete(cls, user):
        db = get_db()
        db.delete(AvailableCar.by_user(user))