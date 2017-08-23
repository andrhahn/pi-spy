import SocketServer
import logging
import threading

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = ''
SOCKET_SERVER_PORT = 8001


class SocketServerRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)

        cur_thread = threading.current_thread()

        response = "{}: {}".format(cur_thread.name, data)

        print 'Connected with client', self.client_address

        print 'Received message: ' + response

        self.request.sendall('Hello govna')


class SocketServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


server = SocketServer((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT), SocketServerRequestHandler)

try:
    print 'Starting socket server on port ', SOCKET_SERVER_PORT

    server.serve_forever()
except KeyboardInterrupt:
    pass

print 'Shutting down socket server...'

server.shutdown()
server.server_close()
