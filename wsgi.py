from flask import render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, join_room, leave_room, emit

from app.main import app

socketio = SocketIO(app, manage_session=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/chat/room/user1/user2', methods=['GET', 'POST'])
def chat():
    # on check si user1 et user2 ont une room (oui -> on get la room | non -> on la crée en db)
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


if __name__ == '__main__':
    socketio.run(app)
