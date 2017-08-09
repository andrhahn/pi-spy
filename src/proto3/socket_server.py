import SocketServer
import io
import logging
import struct
import threading

import PIL.Image

import config

logging.basicConfig(level=logging.DEBUG)


class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'process socket connections thread:', threading.current_thread().name

        try:
            mf = self.request.makefile('rb')

            while True:
                image_len = struct.unpack('<L', mf.read(struct.calcsize('<L')))[0]

                if not image_len:
                    break

                image_stream = io.BytesIO()

                image_stream.write(mf.read(image_len))

                image_stream.seek(0)

                image = PIL.Image.open(image_stream)

                image.verify()

                print 'image verified.'

                image_stream.seek(0)

        finally:
            print 'Disconnected with client'


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    socket_server_port = int(config.get('socket_server_port'))

    print 'Starting socket server on port ', socket_server_port

    socket_server = ThreadedTCPServer((config.get('socket_server_host'), socket_server_port), RequestHandler)

    try:
        socket_server.serve_forever()
    except KeyboardInterrupt:
        pass

        print 'Stopping socket server'

    socket_server.shutdown()
    socket_server.server_close()
