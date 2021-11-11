import socketserver
from http.server import BaseHTTPRequestHandler
import os
import requests
from requests.models import HTTPError

port = os.environ.get('PORT', 8080)
logs_api_endpoint = os.environ.get('LOGS_API_ENDPOINT')


class headerlessLogAPI:

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint

    def send_message(self, data):
        try:
            repsonse = requests.post(url=self.endpoint, data=data)
            print(f"headerlessLogAPI: status code: {repsonse.status_code}")
        except HTTPError as e:
            print(e)


class HttpHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path == '/logs':
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(post_body)
            logs_api.send_message(data=post_body)

        self.send_response(message="POST",code=200)


logs_api = headerlessLogAPI(endpoint=logs_api_endpoint)
httpd = socketserver.TCPServer(("", int(port)), HttpHandler)
httpd.serve_forever()