import SocketServer
import io
import logging
import struct
import threading
import time

import PIL.Image

logging.basicConfig(level=logging.DEBUG)

frame = None


class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global frame

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

                image_stream.seek(0)

                ##frame = image_stream

                print 'Received image:', image.size
        finally:
            print 'Disconnected with client'


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    server = ThreadedTCPServer(('localhost', 8001), RequestHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print 'Starting server on port ', 8001

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

        print 'Stopping server'

    server.shutdown()
    server.server_close()
