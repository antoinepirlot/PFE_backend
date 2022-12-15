from app.main import app
from app.main import socketio

app = socketio.run(app)

if __name__ == "__main__":
    socketio.run(app)
