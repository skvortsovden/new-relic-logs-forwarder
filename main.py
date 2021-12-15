import socketserver
from http.server import BaseHTTPRequestHandler
import os
import requests
from requests.models import HTTPError
import re
import json 

# Proxy server PORT to listen
port = os.environ.get('PORT', 8080)
# New Relic Logs API HTTP endpoint 
logs_api_endpoint = os.environ.get('LOGS_API_ENDPOINT')


# New Relic Logs API
class HeaderlessLogAPI:

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint
    
    # Send message to Logs API endpoint
    def send_message(self, data):
        try:
            print(f"headerlessLogAPI send_message")
            # Decode data
            decoded_data = data.decode('utf8').replace("'", '"')

            # Retrieve JSON object from incoming data
            json_data = re.search('{(.*)}', decoded_data)
            json_string = "{" + json_data.group(1)+ "}"
            json_object = json.loads(json_string)

            # Send retrieved JSON with POST request to Logs API endpoint
            repsonse = requests.post(url=self.endpoint, json=json_object)

            # Print response
            print(f"headerlessLogAPI response status code: {repsonse.status_code}")
            print(f"headerlessLogAPI response text: {repsonse.text}")
        except HTTPError as e:
            # Print error
            print(e)


# HTTP Request Handler
class HttpHandler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        # This just generates an HTML document that includes `message`
        # the body. Override, or re-write this do do more interesting stuff.
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!

    # Handle GET request
    def do_GET(self):
        self._set_headers()
        self.wfile.write(self._html("new-relic-logs-forwarder"))

    # Handle HEAD request
    def do_HEAD(self):
        self._set_headers()

    # Handle POST request
    def do_POST(self):
        self._set_headers()
        if self.path == '/logs':
            content_len = int(self.headers.get('Content-Length'))
            # Retrieve POST request BODY
            post_body = self.rfile.read(content_len)
            print(post_body)
            # Send POST request BODY to Logs API
            logs_api.send_message(data=post_body)

        self.send_response(message="POST",code=200)


logs_api = HeaderlessLogAPI(endpoint=logs_api_endpoint)
httpd = socketserver.TCPServer(("", int(port)), HttpHandler)
httpd.serve_forever()