import BaseHTTPServer
import logging
import os
import socket
import time

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

HTTP_SERVER_HOST = ''
HTTP_SERVER_PORT = 8000


class Observable(object):
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer(*args, **kwargs)


class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
            self.end_headers()

            count = 1

            try:
                while True:
                    if count % 2 == 0:
                        file_name = '/Users/andrhahn/1.jpg'

                    else:
                        file_name = '/Users/andrhahn/2.jpg'

                    f = open(file_name, 'rb')

                    data = f.read()

                    self.wfile.write('--frame')

                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', os.path.getsize(file_name))
                    self.end_headers()

                    self.wfile.write(data)

                    f.close()

                    time.sleep(2)

                    count += 1
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

http_server = BaseHTTPServer.HTTPServer((HTTP_SERVER_HOST, HTTP_SERVER_PORT), HttpRequestHandler)

try:
    print 'Starting socket connection on port ', SOCKET_SERVER_PORT

    socket_connection.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))

    print 'Starting http server on port ', HTTP_SERVER_PORT

    http_server.serve_forever()
except KeyboardInterrupt:
    pass

print 'Shutting down socket connection...'

socket_connection.close()

print 'Shutting down http server...'

http_server.server_close()
