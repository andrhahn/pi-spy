import SocketServer
import logging
import sys
import threading

logging.basicConfig(level=logging.DEBUG)


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, data)

        print 'Connected with client', self.client_address

        print 'Received message: ' + response

        self.request.sendall('Hello govna')


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


server = ThreadedTCPServer(('', 8000), ThreadedTCPRequestHandler)

server_thread = threading.Thread(target=server.serve_forever)

server_thread.daemon = True

server_thread.start()

print 'Server started'

try:
    server.serve_forever()
except KeyboardInterrupt:
    print "Shutting down server..."

    server.shutdown()

    server.server_close()

    sys.exit(0)
