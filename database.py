import couchdb
from flask import g
from config import cloudant_data
from welcome import app
class Database:
    def __init__(self):
        if not hasattr(g, 'db'):
            server = couchdb.Server("https://"+cloudant_data['user']+':'+cloudant_data['password']+'@'+cloudant_data['host']+':'+cloudant_data['port'])
            with app.app_context():
            	try:
                    g.db = server.create('hitchhike')
                except:
                    g.db = server['hitchhike']        
                self.db=g.db
    def getDB(self):
        return self.db
