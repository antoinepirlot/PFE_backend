from flask import Flask, jsonify, request, render_template, session, url_for, redirect
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_cors import CORS

from routes import courses, users

app = Flask(__name__)
cors = CORS(app)

app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config['SESSION_TYPE'] = 'filesystem'

socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat/room/user1/user2', methods=['GET', 'POST'])
def chat():
    # on check si user1 et user2 ont une room (oui -> on get la room | non -> on la crée)
    if request.method == 'POST':
        username = request.form['username']
        room = request.form['room']
        # Store the data in session
        session['username'] = username
        session['room'] = room
        return render_template('chat.html', session=session)
    else:
        if session.get('username') is not None:
            return render_template('chat.html', session=session)
        else:
            return redirect(url_for('index'))


@socketio.on('join', namespace='/chat')
def join(message):
    # si user n'est pas present dans la room -> tu t'en va
    room = session.get('room')
    join_room(room)
    emit('joinStatus', {'msg': session.get('username')}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('leftStatus', {'msg': username}, room=room)


# Routes
app.register_blueprint(courses.route, url_prefix="/courses")
app.register_blueprint(users.route, url_prefix="/users")

if __name__ == '__main__':
    socketio.run(app)
