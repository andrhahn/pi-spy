import io
import os


def copy_file_to_stream(input_file_name):
    """Copies a file fto a stream"""

    input_file = open(input_file_name, 'rb')

    stream = io.BytesIO()

    l = input_file.read(1024)

    while l:
        stream.write(l)

        l = input_file.read(1024)

    stream_size = stream.tell()

    stream.write('\r\n\r\n'.encode('UTF-8'))

    return stream, stream_size


def copy_file_with_stream(input_file_name, output_file_name):
    """Copies a file from the file system into an output file on the file system using streams"""

    input_file = open(input_file_name, 'rb')

    stream = io.BytesIO()

    l = input_file.read(1024)

    with open(output_file_name, 'w') as output_file:
        while l:
            output_file.write(l)
            stream.write(l)

            l = input_file.read(1024)

    output_file.close()

    input_file.close()

    assert os.path.getsize(output_file_name) == stream.tell()


def write_bytes_to_socket(socket_connection, file_name):
    """Writes a file's bytes from a file on the file system to a socket connection"""

    input_file = open(file_name, 'rb')

    l = input_file.read()

    while l:
        socket_connection.send(l)

        l = input_file.read(1024)

    input_file.close()


def write_file_to_http_wfile(base_http_request_handler, file_name):
    input_file = open(file_name, 'rb')

    data = input_file.read()

    base_http_request_handler.wfile.write(data)

    input_file.close()


def write_file_to_http_wfile_with_streams(base_http_request_handler, file_name):
    input_file = open(file_name, 'rb')

    l = input_file.read()

    while l:
        base_http_request_handler.wfile.write(l)

        l = input_file.read(1024)

    input_file.close()


def write_image_stream_to_http_wfile_with_streams(base_http_request_handler, image_stream):
    l = image_stream.read(1024)

    with open('/Users/andrhahn/out1.jpg', 'w') as output_file:
        while l:
            output_file.write(l)

            l = image_stream.read(1024)

    output_file.close()

    write_file_to_http_wfile(base_http_request_handler, '/Users/andrhahn/out1.jpg')


def write_image_stream_to_file(file_name, image_stream):
    l = image_stream.read(1024)

    with open(file_name, 'w') as output_file:
        while l:
            output_file.write(l)

            l = image_stream.read(1024)

    output_file.close()
