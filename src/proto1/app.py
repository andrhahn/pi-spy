import Queue
import io
import logging
import select
import socket
import struct
import threading

from flask import Flask, Response

import config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

my_queue = Queue.Queue()


def generate():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + my_queue.get().read() + b'\r\n')


@app.route('/')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def process_socket_connections():
    ready_to_read, ready_to_write, has_errors = select.select([socket_server], [], [])

    conn = ready_to_read[0].accept()[0].makefile('rb')

    while True:
        image_len = struct.unpack('<L', conn.read(struct.calcsize('<L')))[0]

        if not image_len:
            break

        image_stream = io.BytesIO()

        image_stream.write(conn.read(image_len))

        image_stream.seek(0)

        my_queue.put(image_stream)


if __name__ == '__main__':
    socket_server_port = int(config.get('socket_server_port'))

    print 'Starting socket server on port ', socket_server_port

    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((config.get('socket_server_host'), socket_server_port))
    socket_server.listen(5)

    sock_listener_thread = threading.Thread(target=process_socket_connections)
    sock_listener_thread.daemon = True
    sock_listener_thread.start()

    try:
        app.run(host=config.get('web_server_host'), port=int(config.get('web_server_port')), debug=False, threaded=True)
    except KeyboardInterrupt:
        pass

    print 'Stopping socket server'

    socket_server.close()
