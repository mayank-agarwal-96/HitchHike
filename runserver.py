import os

from HitchHike.welcome import app

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port),debug=True)
