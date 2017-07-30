import io
import socket
import struct
import time
import config

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_server_port = int(config.get('socket_server_port'))

sock.connect((config.get('socket_server_host'), socket_server_port))

conn = sock.makefile('wb')

print 'Connected to socket server on port:', socket_server_port

if __name__ == "__main__":
    try:
        stream = io.BytesIO()

        frames = [open('1.jpg', 'rb').read(), open('2.jpg', 'rb').read(), open('3.jpg', 'rb').read()]

        while True:
            stream.write(frames[1])

            conn.write(struct.pack('<L', stream.tell()))

            conn.flush()

            stream.seek(0)

            conn.write(stream.read())

            stream.seek(0)

            stream.truncate()

            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    conn.write(struct.pack('<L', 0))

    conn.close()
    sock.close()
