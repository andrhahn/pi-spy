import logging
import socket

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print 'Starting socket connection on port ', SOCKET_SERVER_PORT

    socket_connection.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))

    socket_connection.sendall('Hello, world')
except KeyboardInterrupt:
    pass

print 'Shutting down socket connection...'

socket_connection.close()
