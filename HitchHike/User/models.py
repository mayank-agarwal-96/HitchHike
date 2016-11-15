import os
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g
from HitchHike.database import DataBase
# from HitchHike.welcome import get_db


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
        db = DataBase.db()
        user = db.get(id,None)
        # print user
        if user is None:
            return None
        
        return cls.wrap(user)
    
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
    def all(cls):
        db = DataBase.db()
        return cls.view(db,'_design/user/_view/all-users')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db = DataBase.db()
        db[self.email] = self._data

    def update(self, name = None, phone = None, email = None, password = None):
        db = DataBase.db()
        if name:
            self.name = name

        if phone:
            self.phone = phone

        if email:
            self.email = email

        if password:
            self.set_password(password)

        self.store(db)


class HitchHiker(User):
    user_type = TextField(default='hitchhiker')
    

    @classmethod
    def get_user(cls, id):
        db = DataBase.db()
        user = db.get(id,None)
        if user is None:
            return None

        return cls.wrap(user)    


class CarDriver(User):
    user_type = TextField(default='car_owner')


    @classmethod
    def get_user(cls, id):
        db = DataBase.db()
        user = db.get(id,None)
        # print user
        if user is None:
            return None
        if user['user_type'] != 'car_owner':
            return None
        
        return cls.wrap(user)


class Vehicle(Document):
    doc_type = TextField(default='vehicle')
    owner = TextField()
    company = TextField()
    model = TextField()
    reg_number = TextField()
    
    def save(self):
        db = DataBase.db()
        self.store(db)

    @classmethod
    def get_by_user(cls, user):
        db = DataBase.db()
        vehicle = cls.view(
                            db,
                            '_design/user/_view/vehicle/',
                            key = user,
                            include_docs=True
                        )
        result = []
        for x in vehicle:
            result.append(x)

        return result[0]

    def update(self, company = None, reg = None, model = None):
        db = DataBase.db()

        if company:
            self.company = company

        if reg:
            self.reg_number = reg

        if model:
            self.model = model

        self.store(db)