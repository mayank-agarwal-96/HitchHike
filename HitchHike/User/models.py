import os
import couchdb

from datetime import datetime
from couchdb.mapping import Document, TextField, DateTimeField, ListField, FloatField, IntegerField, BooleanField

class User(Document):
    name = TextField()
    username = TextField()
    email = TextField()
    password = TextField()
    dob = DateTimeField(default = None)
    phone = IntegerField()
    gender = BooleanField()
    created = DateTimeField(default=datetime.now)
    category = TextField(default='User')


