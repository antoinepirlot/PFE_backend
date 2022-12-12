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
def user_sign_in(id_user1, id_user2, methods=['GET', 'POST']):
    user1 = users_service.get_users_by_id(id_user1)
    user2 = users_service.get_users_by_id(id_user2)

    chat_room = chat_rooms_service.get_chat_room(id_user1, id_user2)
    if chat_room is None:
        chat_room = chat_rooms_service.create_chat_room(id_user1, id_user2)

    session['username'] = user1.pseudo
    session['room'] = chat_room.id_room
    socketio.emit('room_id', {'room_id': chat_room.id_room, 'username1': user1.pseudo, 'username2': user2.pseudo})


@socketio.on('join')
def join(username, room):
    join_room(room)
    print("on envoie le statut")
    socketio.emit('status', {'msg': username + ' vient de se connecter.'}, room=room)


@socketio.on('left')
def join(username):
    room = session.get('room')
    leave_room(room)
    socketio.emit('status', {'msg': session.get('username') + ' vient de se déconnecter.'}, room=room)


@socketio.on('message')
def messaging(message, methods=['GET', 'POST']):
    print('received message: ' + str(message))
    message['from'] = request.sid
    socketio.emit('message', message, room=request.sid)
    socketio.emit('message', message, room=message['to'])
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ":" + message['msg']}, room=room)


if __name__ == '__main__':
    socketio.run(app)
