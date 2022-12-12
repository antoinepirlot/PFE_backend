from flask import render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit
from services.ChatRoomsService import ChatRoomsService
from services.UsersService import UsersService
from app.main import app
from flask_cors import CORS

socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")
CORS(app)
cors = CORS(app)
chat_rooms_service = ChatRoomsService()
users_service = UsersService()

users = {}


@socketio.on('connect')
def on_connect():
    print('Client connected')
    socketio.emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def on_disconnect():
    users.pop(request.sid, 'No user found')
    socketio.emit('current_users', users)
    print("User disconnected!\nThe users are: ", users)


@socketio.on('sign_in')
def user_sign_in(user_name, methods=['GET', 'POST']):
    users[request.sid] = user_name['name']
    socketio.emit('current_users', users)
    print("New user sign in!\nThe users are: ", users)


@socketio.on('message')
def messaging(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    message['from'] = request.sid
    socketio.emit('message', message, room=request.sid)
    socketio.emit('message', message, room=message['to'])


if __name__ == '__main__':
    socketio.run(app)
