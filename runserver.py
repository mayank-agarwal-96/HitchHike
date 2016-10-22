import os

from HitchHike.welcome import app,socketio
from mysocket import MyNamespace 
port = os.getenv('PORT', '5000')
socketio.on_namespace(MyNamespace('/test'))
if __name__ == "__main__":
	socketio.run(app)
	
