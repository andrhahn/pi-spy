import logging
import socket
import threading
import time

from flask import Flask, Response

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


class SocketClient(object):
    thread = None
    frame = None

    def initialize(self):
        if SocketClient.thread is None:
            SocketClient.thread = threading.Thread(target=self._thread)
            SocketClient.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        self.initialize()

        return self.frame

    @classmethod
    def _thread(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8002))

        print 'Connected to socket server'

        try:
            while True:
                stream = sock.recv(1024)  # todo: get stream with all the pieces and assemble

                if stream:
                    print 'received part of stream...'
                    # cls.frame = stream.read()
                else:
                    time.sleep(1)
        finally:
            sock.close()

            cls.thread = None


def gen(socket_client):
    while True:
        frame = socket_client.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video-feed')
def video_feed():
    socket_client = SocketClient()

    return Response(gen(socket_client), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='localhost', port=8000, debug=True, threaded=True)
