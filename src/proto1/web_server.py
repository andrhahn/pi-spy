import logging

from flask import Flask, Response

from socket_client import SocketClient

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def gen(socket_client):
    while True:
        frame = socket_client.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video-feed')
def video_feed():
    return Response(gen(SocketClient()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True, threaded=True)
