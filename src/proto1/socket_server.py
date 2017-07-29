import SocketServer
import io
import logging
import struct
import threading
import time

import PIL.Image

logging.basicConfig(level=logging.DEBUG)

frame = None


class UploadRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global frame

        print 'Connected with client for upload'

        mf = self.request.makefile('rb')

        try:
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

                frame = image_stream

                print 'Received image:', image.size
        finally:
            print 'Connection with client lost'


class DownloadRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        global frame

        print 'Connected with client for download'

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

            frame = image_stream

            print 'Received image:', image.size


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


def start_server(host, port, handler):
    server = ThreadedTCPServer((host, port), handler)

    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print 'Starting server on port ', port

    return server


def stop_server(server):
    print 'Stopping server'

    server.shutdown()
    server.server_close()


if __name__ == "__main__":
    upload_server = start_server('localhost', 8001, UploadRequestHandler)
    download_server = start_server('localhost', 8002, DownloadRequestHandler)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    stop_server(upload_server)
    stop_server(download_server)
