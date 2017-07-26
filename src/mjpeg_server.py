import BaseHTTPServer
import logging
import os
import time

logging.basicConfig(level=logging.DEBUG)


class MyRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=boundarydonotcross')
            self.end_headers()

            count = 1

            try:
                while True:
                    if count % 2 == 0:
                        file_name = 'c:/temp/1.jpg'

                    else:
                        file_name = 'c:/temp/2.jpg'

                    f = open(file_name, 'rb')

                    self.wfile.write('--boundarydonotcross')

                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', os.path.getsize(file_name))
                    self.end_headers()

                    self.wfile.write(f.read())

                    f.close()

                    time.sleep(2)

                    count += 1
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


server = BaseHTTPServer.HTTPServer(('', 8000), MyRequestHandler)

try:
    print 'Server started'

    server.serve_forever()
except KeyboardInterrupt:
    pass

finally:
    print 'Shutting down server...'

    server.server_close()
