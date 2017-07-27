import logging
import socket

logging.basicConfig(level=logging.DEBUG)


class SocketClient:
    def __init__(self, host, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        print 'Connected to socket server on port ', port

    def get_frame(self):
        try:
            while True:
                return self.s.recv(1024)
        finally:
            self.close()

    def close(self):
        self.s.close()

        print 'Shutting down socket connection...'
