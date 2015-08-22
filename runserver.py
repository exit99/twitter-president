from app import create_app
from extensions import socketio


app = create_app()
socketio.run(app)
