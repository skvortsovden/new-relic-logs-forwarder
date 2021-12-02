import socketserver
from http.server import BaseHTTPRequestHandler
import os
import requests
from requests.models import HTTPError
import re
import json 

port = os.environ.get('PORT', 8080)
logs_api_endpoint = os.environ.get('LOGS_API_ENDPOINT')

class HeaderlessLogAPI:

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint

    def send_message(self, data):
        try:
            print(f"headerlessLogAPI send_message")
            decoded_data = data.decode('utf8').replace("'", '"')
            json_data = re.search('{(.*)}', decoded_data)
            json_string = "{" + json_data.group(1)+ "}"
            json_object = json.loads(json_string)
            repsonse = requests.post(url=self.endpoint, json=json_object)
            print(f"headerlessLogAPI response status code: {repsonse.status_code}")
            print(f"headerlessLogAPI response text: {repsonse.text}")
        except HTTPError as e:
            print(e)


class HttpHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("new-relic-logs-forwarder"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        if self.path == '/logs':
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(post_body)
            logs_api.send_message(data=post_body)

        self.send_response(message="POST",code=200)


logs_api = HeaderlessLogAPI(endpoint=logs_api_endpoint)
httpd = socketserver.TCPServer(("", int(port)), HttpHandler)
httpd.serve_forever()