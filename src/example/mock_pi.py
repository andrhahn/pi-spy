import logging
import socket

import utils

logging.basicConfig(level=logging.DEBUG)

SOCKET_SERVER_HOST = 'localhost'
SOCKET_SERVER_PORT = 8001

if __name__ == "__main__":
    socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print 'Starting socket connection on port ', SOCKET_SERVER_PORT

        socket_connection.connect((SOCKET_SERVER_HOST, SOCKET_SERVER_PORT))

        #while True:
            #print 'Writing file'

        utils.write_bytes_to_socket(socket_connection, '/Users/andrhahn/2.jpg')

            #time.sleep(2)

    except KeyboardInterrupt:
        pass

    print 'Shutting down socket connection...'

    socket_connection.close()
