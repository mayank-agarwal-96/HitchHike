import os

from HitchHike.welcome import app, socketio
from flask_socketio import SocketIO

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	print "afa"
	# app.run(host='0.0.0.0', port=int(port),debug=True)
	# socketio = SocketIO(app)
	socketio.run(app, host='0.0.0.0', port=int(port), debug=True)