from app.main import app, socketio

start = socketio.run(app)

if __name__ == "__main__":
    socketio.run(app)
