import BaseHTTPServer
import SocketServer
import logging
import os
import threading
import time

logging.basicConfig(level=logging.DEBUG)


class SocketServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)

        print 'Connected with client', self.client_address

        print 'Received message: ' + response

        self.request.sendall('Hello govna')


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

                    self.wfile.write('--frame')

                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', os.path.getsize(file_name))
                    self.end_headers()

                    self.wfile.write(f.read())

                    f.close()

                    time.sleep(2)

                    count += 1
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class SocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


http_server = BaseHTTPServer.HTTPServer(('', 8000), HttpRequestHandler)

socket_server = SocketServer(('', 8001), SocketServerRequestHandler)

try:
    print 'Starting socket server...'

    socket_server_thread = threading.Thread(target=socket_server.serve_forever)
    socket_server_thread.daemon = True
    socket_server_thread.start()

    print 'Starting http server'

    http_server.serve_forever()
except KeyboardInterrupt:
    pass
finally:
    print 'Shutting down socket server...'

    socket_server.shutdown()
    socket_server.server_close()

    print 'Shutting down http server...'

    http_server.server_close()
