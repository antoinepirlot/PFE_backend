from flask import Flask, session
from flask_cors import CORS
from flask_socketio import join_room, leave_room, SocketIO

from Exceptions.FatalException import FatalException
from Exceptions.WebExceptions.BadRequestException import BadRequestException
from Exceptions.WebExceptions.ConflictException import ConflictException
from Exceptions.WebExceptions.ForbiddenException import ForbiddenException
from Exceptions.WebExceptions.NotFoundException import NotFoundException
from Exceptions.WebExceptions.UnauthorizedException import UnauthorizedException
from routes import courses, users, ratings, favorites, authentications, notifications, chat_rooms, categories, \
    appointments

app = Flask(__name__)
cors = CORS(app)
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
app.register_blueprint(chat_rooms.route, url_prefix="/chat_rooms")
app.register_blueprint(categories.route, url_prefix="/categories")
app.register_blueprint(appointments.route, url_prefix="/appointments")


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


if __name__ == '__main__':
    app.run()
