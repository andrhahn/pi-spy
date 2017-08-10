import Queue
import io
import logging
import threading

import PIL.Image
import pika
from flask import Flask, Response

import config

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

queue = Queue.Queue(1)


def populate_queue():
    def callback(ch, method, properties, body):
        image_stream = io.BytesIO()

        image_stream.write(body)

        image_stream.seek(0)

        image = PIL.Image.open(image_stream)

        image.verify()

        image_stream.seek(0)

        queue.put(image_stream)

    queue_channel.basic_consume(callback, queue=queue_name, no_ack=True)

    queue_channel.start_consuming()


def generate():
    while True:
        image_stream = queue.get()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_stream.read() + b'\r\n')


@app.route('/')
def index():
    print 'Connected client on thread:', threading.current_thread().name

    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    print 'Connecting to queue server'

    queue_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=config.get('queue_server_host'), port=int(config.get('queue_server_port'))))

    queue_channel = queue_connection.channel()

    queue_channel.exchange_declare(exchange='images', exchange_type='fanout')

    result = queue_channel.queue_declare(exclusive=True)

    queue_name = result.method.queue

    queue_channel.queue_bind(exchange='images', queue=queue_name)

    socket_server_thread = threading.Thread(target=populate_queue)
    socket_server_thread.daemon = True
    socket_server_thread.start()

    try:
        print 'Started web server on main thread:', threading.current_thread().name

        app.run(host=config.get('web_server_host'), port=int(config.get('web_server_port')), threaded=True, debug=False)
    except KeyboardInterrupt:
        pass

    print 'Closing queue connection'

    queue_connection.close()
