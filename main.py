import socketserver
from http.server import BaseHTTPRequestHandler
import os

class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/logs':
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(post_body)

        self.send_response(message="POST",code=200)

port = os.environ.get('PORT', 8080)
httpd = socketserver.TCPServer(("", int(port)), HttpHandler)
httpd.serve_forever()