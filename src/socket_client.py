import logging
import socket

logging.basicConfig(level=logging.DEBUG)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print 'Socket created'

try:
    s.connect(('localhost', 8000))

    s.sendall('Hello gov')

    resp = s.recv(1024)

    print 'Received message from server: ' + resp
finally:
    s.close()

    print 'Socket closed'
