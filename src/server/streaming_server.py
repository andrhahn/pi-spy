import BaseHTTPServer
import SocketServer
import io
import logging
import os
import threading
import time
from abc import ABCMeta, abstractmethod

from PIL import Image

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

    def unregister_observer(self, observer):
        if observer in self.__observers:
            self.__observers.remove(observer)

    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(*args, **kwargs)


class Observer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, *args, **kwargs):
        pass


class FrameChangeObservable(Observable, object):
    pass


class FrameChangeObserver(Observer):
    # def __init__(self):
    #     self.frame = []

    def notify(self, *args, **kwargs):
        print 'received event:', args[0]

        image_stream = kwargs['image_stream']

        image_stream.seek(0)

        image = Image.open(image_stream)

        print('Image is %dx%d' % image.size)

        image.verify()


observable = FrameChangeObservable()


class SocketServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'recevied socket request'

        l = self.request.recv(1024)

        image_stream = io.BytesIO()

        while l:
            print "Receiving..."

            image_stream.write(l)

            l = self.request.recv(1024)

        image_stream.seek(0)

        image = Image.open(image_stream)

        print('Image is %dx%d' % image.size)

        image.verify()

        print "Done Receiving"

        # cur_thread = threading.current_thread()

        # response = "{}: {}".format(cur_thread.name, data)

        observable.notify_observers('New image to process', image_stream=image_stream)

        # print 'Connected with client', self.client_address

        # print 'Received message: ' + response

        # self.request.sendall('Hello govna')


class SocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


class HttpRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            observer = FrameChangeObserver()

            observable.register_observer(observer)

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

                    ####img = Image.open()

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
