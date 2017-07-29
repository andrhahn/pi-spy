import io
import logging
import socket
import struct
import thread

import PIL.Image

logging.basicConfig(level=logging.DEBUG)


def handler(conn):
    print 'Connected with client'

    try:
        while True:
            image_len = struct.unpack('<L', conn.read(struct.calcsize('<L')))[0]

            if not image_len:
                break

            image_stream = io.BytesIO()

            image_stream.write(conn.read(image_len))

            image_stream.seek(0)

            image = PIL.Image.open(image_stream)

            image.verify()

            print 'Received image:', image.size
    finally:
        conn.close()


if __name__ == "__main__":
    server_sock = socket.socket()

    server_sock.bind(('localhost', 8001))

    server_sock.listen(0)

    print 'Starting socket server on port ', 8001

    try:
        while True:
            print 'Waiting for connection...'

            thread.start_new_thread(handler, (server_sock.accept()[0].makefile('rb'),))
    except KeyboardInterrupt:
        pass

    print 'Shutting down socket server...'

    server_sock.close()
