import Queue
import io
import logging
import select
import socket
import struct
import threading
import uuid
import time

from flask import Flask, Response

import config

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

connected_clients = []


def generate(connected_client):
    while True:
        time.sleep(5)

        print 'queue size at time of generate():', connected_client['queue'].qsize()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + connected_client['queue'].get().read() + b'\r\n')


@app.route('/')
def index():
    print 'Connected client: ', uuid.uuid4(), 'on thread:', threading.current_thread().name

    time.sleep(100)

    connected_client = {'id': uuid.uuid4(), 'queue': Queue.Queue(50)}

    connected_clients.append(connected_client)

    return Response(generate(connected_client), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def hello_world():
    print 'Connected client: ', uuid.uuid4(), 'on thread:', threading.current_thread().name

    return 'Hello, World!'


# def process_socket_connections():
#     ready_to_read, ready_to_write, has_errors = select.select([socket_server], [], [])
#
#     print 'process socket connections thread:', threading.current_thread().name
#
#     print 'ready to read...'
#
#     conn = ready_to_read[0].accept()[0].makefile('rb')
#
#     while True:
#         image_len = struct.unpack('<L', conn.read(struct.calcsize('<L')))[0]
#
#         if not image_len:
#             break
#
#         image_stream = io.BytesIO()
#
#         image_stream.write(conn.read(image_len))
#
#         image_stream.seek(0)
#
#         for connected_client in connected_clients:
#                 try:
#                     connected_client['queue'].put_nowait(image_stream)
#                 except Queue.Full:
#                     print 'queue is full!'


if __name__ == '__main__':
    socket_server_port = int(config.get('socket_server_port'))

    print 'Starting socket server on port ', socket_server_port

    # socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket_server.bind((config.get('socket_server_host'), socket_server_port))
    # socket_server.listen(5)

    # sock_listener_thread = threading.Thread(target=process_socket_connections)
    #sock_listener_thread.daemon = True
    #sock_listener_thread.start()

    try:
        print 'main thread:', threading.current_thread().name

        app.run(host=config.get('web_server_host'), port=int(config.get('web_server_port')))
    except KeyboardInterrupt:
        pass

    print 'Stopping socket server'

    # socket_server.close()
