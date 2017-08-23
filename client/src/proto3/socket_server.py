import SocketServer
import io
import logging
import struct
import threading

import PIL.Image
import pika

import config

logging.basicConfig(level=logging.INFO)


class RequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print 'Process socket connections thread:', threading.current_thread().name

        try:
            mf = self.request.makefile('rb')

            while True:
                image_len = struct.unpack('<L', mf.read(struct.calcsize('<L')))[0]

                image_bytes = mf.read(image_len)

                if not image_len:
                    break

                image_stream = io.BytesIO()

                image_stream.write(image_bytes)

                image_stream.seek(0)

                image = PIL.Image.open(image_stream)

                image.verify()

                print 'Image verified.'

                queue_channel = queue_connection.channel()

                queue_channel.exchange_declare(exchange='images', exchange_type='fanout')

                queue_channel.basic_publish(exchange='images', routing_key='', body=image_bytes)

                print 'Sent image.'

        finally:
            print 'Disconnected with client'


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    print 'Connecting to queue server'

    queue_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.get('queue_server_host'), port=int(config.get('queue_server_port'))))

    socket_server_port = int(config.get('socket_server_port'))

    print 'Starting socket server on port ', socket_server_port

    socket_server = ThreadedTCPServer((config.get('socket_server_host'), socket_server_port), RequestHandler)

    try:
        socket_server.serve_forever()
    except KeyboardInterrupt:
        pass

    print 'Closing queue connection'

    queue_connection.close()

    print 'Stopping socket server'

    socket_server.shutdown()
    socket_server.server_close()
