import couchdb
import os

from config import cloudant_data

class DataBase:
    _url = "https://"+cloudant_data['user']+':'+cloudant_data['password']+'@'+cloudant_data['host']+':'+cloudant_data['port']
    _name = "hitchhike"
    _db = None
    _server = None

    @classmethod
    def db(cls):
        cls._server = couchdb.Server(cls._url)
        cls._db = cls._server(cls._name)

        return cls._db