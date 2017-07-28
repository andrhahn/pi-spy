import logging
import os
import socket
import struct

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print 'Starting socket connection on port ', SOCKET_SERVER_PORT

    socket_connection.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))

    # todo: first just send a single file.  next, send real frames to socket server

    file_name = '/Users/andrhahn/1.jpg'

    f = open(file_name, 'rb')

    #socket_connection.send(struct.pack('<L', os.path.getsize(file_name)))

    l = f.read(1024)

    while l:
        print 'Sending...'

        socket_connection.send(l)

        l = f.read(1024)

    f.close()

    #socket_connection.send(struct.pack('<L', 0))


    # count = 1

    # while True:
    #     if count % 2 == 0:
    #         file_name = '/Users/andrhahn/1.jpg'
    #
    #     else:
    #         file_name = '/Users/andrhahn/2.jpg'
    #
    #     f = open(file_name, 'rb')
    #
    #     l = f.read(1024)
    #
    #     while (l):
    #         print 'Sending...'
    #
    #         socket_connection.send(l)
    #
    #         l = f.read(1024)
    #
    #     f.close()
    #
    #     #data = f.read()
    #
    #     #socket_connection.send(data)
    #
    #     f.close()
    #
    #     time.sleep(2)
    #
    #     count += 1
except KeyboardInterrupt:
    pass

print 'Shutting down socket connection...'

socket_connection.close()
