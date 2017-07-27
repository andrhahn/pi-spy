import BaseHTTPServer
import logging
import os
import socket
import time

from PIL import Image

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

HTTP_SERVER_HOST = ''
HTTP_SERVER_PORT = 8000


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
                        file_name = 'c:/temp/1.jpg'

                    else:
                        file_name = 'c:/temp/2.jpg'

                    f = open(file_name, 'rb')

                    image = Image.open(f)

                    print 'Image size: ', image.size

                    f.close()

                    f = open(file_name, 'rb')

                    data = f.read()

                    buf = socket_connection.recv(1024)

                    if buf.startswith(b'\xff\xd8'):
                        print 'foo'
                    else:
                        print 'bar'

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
