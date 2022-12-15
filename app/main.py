from flask import Flask, session, request
from flask_cors import CORS
from flask_socketio import join_room, leave_room, SocketIO
from services.ChatRoomsService import ChatRoomsService
from services.UsersService import UsersService
from Exceptions.FatalException import FatalException
from Exceptions.WebExceptions.BadRequestException import BadRequestException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from Exceptions.WebExceptions.UnauthorizedException import UnauthorizedException
from routes import courses, users, ratings, favorites, authentications, notifications, categories, \
    appointments

app = Flask(__name__)
cors = CORS(app)
chat_rooms_service = ChatRoomsService()
users_service = UsersService()

socketio = SocketIO(app, manage_session=False, cors_allowed_origins="*")

app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

# Routes
app.register_blueprint(courses.route, url_prefix="/courses")
app.register_blueprint(users.route, url_prefix="/users")
app.register_blueprint(ratings.route, url_prefix="/ratings")
app.register_blueprint(favorites.route, url_prefix="/favorites")
app.register_blueprint(notifications.route, url_prefix="/notifications")
app.register_blueprint(authentications.route, url_prefix="/authentications")
app.register_blueprint(categories.route, url_prefix="/categories")
app.register_blueprint(appointments.route, url_prefix="/appointments")


#Socket
@socketio.on('connect')
def on_connect():
    socketio.emit('my response', {'data': 'Connected'})


@socketio.on('sign_in')
def user_sign_in(id_user1, id_user2, methods=['GET', 'POST']):
    user1 = users_service.get_users_by_id(id_user1)
    user2 = users_service.get_users_by_id(id_user2)

    #chat_room = chat_rooms_service.get_chat_room(id_user1, id_user2)
    #if chat_room is None:

    chat_room = chat_rooms_service.create_chat_room(id_user1, id_user2)

    session['username'] = user1.pseudo
    session['room'] = chat_room.id_room
    socketio.emit('room_id', {'room_id': chat_room.id_room, 'username1': user1.pseudo, 'username2': user2.pseudo})


@socketio.on('join')
def join(username, room):
    join_room(room)
    socketio.emit('status', {'msg': username + ' vient de se connecter.'}, room=room)


@socketio.on('left')
def left(username, room):
    leave_room(room)
    session.clear()
    print(username, ' a quitter la conv')
    socketio.emit('statusLeft', {'msg': username + ' vient de se déconnecter.'}, room=room)


@socketio.on('message')
def messaging(message, id_room, username, methods=['GET', 'POST']):
    room = id_room
    socketio.emit('message', {'msg': username + ":" + message}, room=room)


@socketio.on('disconnect')
def on_disconnect():
    users.pop(request.sid, 'No user found')
    socketio.emit('current_users', users)
    #print("User disconnected!\nThe users are: ", users)



# Exceptions
@app.errorhandler(BadRequestException)
def bad_request_exception(e):
    return str(e), 400


@app.errorhandler(UnauthorizedException)
def unauthorized_exception(e):
    return str(e), 401


@app.errorhandler(ForbiddenException)
def forbidden_exception(e):
    return str(e), 403


@app.errorhandler(NotFoundException)
def not_found_exception(e):
    return str(e), 404


@app.errorhandler(ConflictException)
def conflict_exception(e):
    return str(e), 409


@app.errorhandler(FatalException)
def fatal_exception(e):
    return str(e), 500


def run():
    socketio.run(app)
