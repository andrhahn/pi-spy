import SocketServer
import io
import logging
import struct
import threading
import time

import PIL.Image
from flask import Flask, Response

import config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

frame = None


class TCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global frame

        try:
            mf = self.request.makefile('rb')

            while True:
                image_len = struct.unpack('<L', mf.read(struct.calcsize('<L')))[0]

                if not image_len:
                    break

                image_stream = io.BytesIO()

                image_stream.write(mf.read(image_len))

                image_stream.seek(0)

                image = PIL.Image.open(image_stream)

                image.verify()

                image_stream.seek(0)

                frame = image_stream

                print 'Received image:', image.size
        finally:
            print 'Disconnected with client'


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def gen():
    while True:
        while frame is None:
            time.sleep(1)

        frame.seek(0)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame.read() + b'\r\n')


@app.route('/')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    socket_server_port = int(config.get('socket_server_port'))

    print 'Starting socket server on port ', socket_server_port

    socket_server = ThreadedTCPServer((config.get('socket_server_host'), socket_server_port), TCPRequestHandler)

    try:
        socket_server_thread = threading.Thread(target=socket_server.serve_forever)
        socket_server_thread.daemon = True
        socket_server_thread.start()

        app.run(host=config.get('web_server_host'), port=int(config.get('web_server_port')), threaded=True)
    except KeyboardInterrupt:
        pass

        print 'Stopping socket server'

        socket_server.shutdown()
        socket_server.server_close()
