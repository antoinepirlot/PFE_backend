from flask import Flask, request, render_template, session, url_for, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

from routes import courses, users

app = Flask(__name__)
cors = CORS(app)

app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'


# Routes
app.register_blueprint(courses.route, url_prefix="/courses")
app.register_blueprint(users.route, url_prefix="/users")

