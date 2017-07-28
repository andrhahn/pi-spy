import BaseHTTPServer
import SocketServer
import io
import logging
import threading
import time

from observable import Observable
from observer import Observer

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

HTTP_SERVER_HOST = ''
HTTP_SERVER_PORT = 8000


class FrameChangeObservable(Observable, object):
    pass


class FrameChangeObserver(Observer):
    def notify(self, *args, **kwargs):
        print 'Received new frame event:', args[0]

        self.callback(kwargs['image_stream'], kwargs['image_size'])


observable = FrameChangeObservable()


class SocketServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'Received socket request'

        image_stream = io.BytesIO()

        l = self.request.recv(1024)

        while l:
            image_stream.write(l)

            l = self.request.recv(1024)

        observable.notify_observers('new.frame.available', image_stream=image_stream, image_size=image_stream.tell())


class SocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def write_frame(self, image_stream, image_size):
        self.wfile.write('--frame')

        self.send_header('Content-Type', 'image/jpeg')
        self.send_header('Content-Length', image_size)
        self.end_headers()

        image_stream.seek(0)

        self.wfile.write(image_stream.read())

    def do_GET(self):
        if self.path == '/':
            try:
                observer = FrameChangeObserver()
                observer.callback = self.write_frame

                self.send_response(200)
                self.send_header('Age', 0)
                self.send_header('Cache-Control', 'no-cache, private')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
                self.end_headers()

                observable.register_observer(observer)

                while True:
                    time.sleep(1)
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


if __name__ == "__main__":
    socket_server = SocketServer((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT), SocketServerRequestHandler)

    http_server = BaseHTTPServer.HTTPServer((HTTP_SERVER_HOST, HTTP_SERVER_PORT), HttpRequestHandler)

    try:
        print 'Starting socket server on port ', SOCKET_SERVER_PORT

        threading = threading.Thread(target=socket_server.serve_forever)
        threading.daemon = True
        threading.start()

        print 'Starting http server on port ', HTTP_SERVER_PORT

        http_server.serve_forever()
    except KeyboardInterrupt:
        pass

    print 'Shutting down socket server...'

    socket_server.shutdown()
    socket_server.server_close()

    print 'Shutting down http server...'

    http_server.server_close()
