import io
import socket
import struct
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8001))

conn = sock.makefile('wb')

print 'Connected to socket server on port', 8001

try:
    stream = io.BytesIO()

    frames = [open('1.jpg', 'rb').read(), open('2.jpg', 'rb').read(), open('3.jpg', 'rb').read()]

    while True:
        stream.write(frames[int(time.time()) % 3])

        conn.write(struct.pack('<L', stream.tell()))

        conn.flush()

        stream.seek(0)

        conn.write(stream.read())

        stream.seek(0)

        stream.truncate()

        time.sleep(0.5)
finally:
    conn.write(struct.pack('<L', 0))

    conn.close()
    sock.close()
