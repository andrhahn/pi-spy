import io

import PIL.Image
import pika

import config

queue_connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=config.get('queue_server_host'), port=int(config.get('queue_server_port'))))

try:
    queue_channel = queue_connection.channel()

    queue_channel.exchange_declare(exchange='images', exchange_type='fanout')

    result = queue_channel.queue_declare(exclusive=True)

    queue_name = result.method.queue

    queue_channel.queue_bind(exchange='images', queue=queue_name)

    print 'Waiting for images.'


    def callback(ch, method, properties, body):
        print 'received message.'

        image_stream = io.BytesIO()

        image_stream.write(body)

        image_stream.seek(0)

        image = PIL.Image.open(image_stream)

        image.verify()

        print 'Image verified.'


    queue_channel.basic_consume(callback, queue=queue_name, no_ack=True)

    queue_channel.start_consuming()
finally:
    queue_connection.close()
