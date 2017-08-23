import socket
import threading
import time


class SocketClient(object):
    thread = None
    frame = None

    def initialize(self):
        if SocketClient.thread is None:
            SocketClient.thread = threading.Thread(target=self._thread)
            SocketClient.thread.start()

            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        self.initialize()

        return self.frame

    @classmethod
    def _thread(cls):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 8002))

        print 'Connected to socket server'

        try:
            while True:
                stream = sock.recv(1024)  # todo: get stream with all the pieces and assemble

                if stream:
                    print 'received part of stream...'
                    # cls.frame = stream.read()
                else:
                    time.sleep(1)
        finally:
            sock.close()

            cls.thread = None
