from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, engineio_logger=app.logger, logger=app.logger)


@app.route("/test")
def test():
    return "HeHe"


@socketio.on('connect')
def on_connect():
    emit('my response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on_error_default
def default_error_handler(e):
    print(e)


if __name__ == '__main__':
    socketio.run(app, log_output=True, debug=True)
