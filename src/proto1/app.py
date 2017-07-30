import SocketServer
import io
import logging
import struct
import threading
import time

import PIL.Image
from flask import Flask, Response

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


if __name__ == '__main__':
    print 'Starting socket server on port ', 8001

    socket_server = ThreadedTCPServer(('localhost', 8001), TCPRequestHandler)

    try:
        socket_server_thread = threading.Thread(target=socket_server.serve_forever)
        socket_server_thread.daemon = True
        socket_server_thread.start()

        app.run(host='localhost', port=8000, threaded=True)
    except KeyboardInterrupt:
        pass

        print 'Stopping socket server'

        socket_server.shutdown()
        socket_server.server_close()
