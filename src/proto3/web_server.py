import io
import logging
import threading

import PIL.Image
import pika
from flask import Flask, Response

import config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


def generate():
    print 'generate() called...'

    def callback(ch, method, properties, body):
        print 'Received message.'

        image_stream = io.BytesIO()

        image_stream.write(body)

        image_stream.seek(0)

        image = PIL.Image.open(image_stream)

        image.verify()

        print 'Image verified.'

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + body + b'\r\n')

    print 'Waiting for images.'

    queue_channel.basic_get(queue=queue_name, no_ack=True)

    print 'a...'

    queue_channel.start_consuming()

    print 'b...'


@app.route('/')
def index():
    print 'Connected client on thread:', threading.current_thread().name

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print 'Connecting to queue server'

    queue_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1', port=int(config.get('queue_server_port'))))

    # queue_channel = queue_connection.channel()
    #
    # queue_channel.exchange_declare(exchange='images', exchange_type='fanout')
    #
    # result = queue_channel.queue_declare(exclusive=True)
    #
    # queue_name = result.method.queue
    #
    # queue_channel.queue_bind(exchange='images', queue=queue_name)
    #
    # print 'Waiting for images.'
    #
    # def callback(ch, method, properties, body):
    #     print 'Received message.'
    #
    #     image_stream = io.BytesIO()
    #
    #     image_stream.write(body)
    #
    #     image_stream.seek(0)
    #
    #     image = PIL.Image.open(image_stream)
    #
    #     image.verify()
    #
    #     print 'Image verified.'
    #
    # queue_channel.basic_consume(callback, queue=queue_name, no_ack=True)
    #
    # print 'a...'
    #
    # queue_channel.start_consuming()
    #
    # print 'b...'

    queue_channel = queue_connection.channel()

    queue_channel.exchange_declare(exchange='images', exchange_type='fanout')

    result = queue_channel.queue_declare(exclusive=True)

    queue_name = result.method.queue

    queue_channel.queue_bind(exchange='images', queue=queue_name)

    try:
        print 'Started web server on main thread:', threading.current_thread().name

        app.run(host=config.get('web_server_host'), port=int(config.get('web_server_port')), threaded=True, debug=False)
    except KeyboardInterrupt:
        pass

    print 'Closing queue connection'

    queue_connection.close()
