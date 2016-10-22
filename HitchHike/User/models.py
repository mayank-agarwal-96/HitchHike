import os
import couchdb
from HitchHike.config import GOOGLE_API_KEY  
from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g

class User(Document):

    doc_type = TextField(default='user')
    name = TextField()
    username = TextField()
    email = TextField()
    password = TextField()
    dob = DateTimeField(default = None)
    phone = IntegerField()
    gender = BooleanField()
    created = DateTimeField(default=datetime.now)


    @classmethod
    def get_user(cls,id):
        db = g.db
        user = db.get(id,None)

        if user is None:
            return None
        
        return cls.wrap(user)
 
    def get_username(self):
        return self.username
        
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email
            

    @classmethod
    def all(cls,db):
        return cls.view(db,'_design/user/_view/all-users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db = g.db
        db[self.email] = self._data
class HitchHiker(User):
    pass
class CarDriver(User):
    pass
class CurrentRequestingHitch():
    hitch_hike_email=TextField()
    car_driver_email=TextField()
    start_point=TextField()
    created = DateTimeField(default=datetime.now)
    
    def check(self,car_location):
        
