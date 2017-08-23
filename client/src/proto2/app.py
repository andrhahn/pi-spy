from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@socketio.on('connect')
def connect():
    print 'Client connected'


@socketio.on('disconnect')
def video_disconnect():
    print 'Client disconnected'


@socketio.on('foo', namespace='/video')
def handle_foo(message):
    print 'Received message on video:', str(message)


if __name__ == '__main__':
    print 'Started server'

    try:
        socketio.run(app, host='localhost', port=8000)
    except KeyboardInterrupt:
        pass

    print 'Shutting down server'
