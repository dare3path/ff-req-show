#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
import json
import time

class EchoServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ['/', '/index.html']:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/xhr.js':
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('xhr.js', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/xhr2.js':
            self.send_response(200)
            self.send_header('Content-type', 'text/javascript')
            self.end_headers()
            with open('xhr2.js', 'rb') as file:
                self.wfile.write(file.read())
        elif self.path == '/ping':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            if self.headers.get('Host') == 'alsonotmyserver.com:8080':
                self.send_header('Access-Control-Allow-Origin', 'http://myserver.com:8080')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(b'pong')
        else:
            self.send_response(404)
            self.end_headers()
    def do_POST(self):
        #if self.path == '/ping':
        if self.path.startswith('/ping'):
            # Get the content length to read the body
            content_length = int(self.headers.get('Content-Length', 0))
            # Read the raw body data
            body = self.rfile.read(content_length).decode('utf-8')

            # Check the Content-Type to handle the data appropriately
            content_type = self.headers.get('Content-Type', '')

            if 'application/x-www-form-urlencoded' in content_type:
                # Parse URL-encoded form data (e.g., "name=John&time=1234567890")
                parsed_data = urllib.parse.parse_qs(body)
                # Flatten the parsed data (since parse_qs returns lists)
                data = {key: value[0] for key, value in parsed_data.items()}
                # Example response using the data
                response = f"Received: name={data.get('name', 'unknown')}, time={data.get('time', 'unknown')}"

            elif 'application/json' in content_type:
                # Parse JSON data (e.g., {"name": "John", "time": 1234567890})
                data = json.loads(body)
                response = f"Received: name={data.get('name', 'unknown')}, time={data.get('time', 'unknown')}"

            else:
                # Fallback for unsupported content types
                response = "Unsupported Content-Type"
                #response = "f"


            host = self.headers.get('Host')
            print(f"Host received: {host}") # Debug
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            if host == 'alsonotmyserver.com:8080':
                self.send_header('Access-Control-Allow-Origin', 'http://myserver.com:8080')
                self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                print(f"CORS headers added for {host}") # Debug
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        if self.path.startswith('/api/statsig/log_event'):
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length).decode('utf-8')
            print(f"Received POST: {body}")
            # Delay to push Firefox into abort territory
            time.sleep(5)  # 2s delay
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            # No CORS headers—keep it blocked
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            print("404");
            self.send_response(404)
            self.end_headers()
    def do_OPTIONS(self):
        if self.path == '/ping' and self.headers.get('Host') == 'alsonotmyserver.com:8080':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', 'http://myserver.com:8080')
            self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            print("sent OPTIONS")
        else:
            self.send_response(404)
            self.end_headers()
            print("sent 404 for OPTIONS")


if __name__ == '__main__':
    host='127.0.0.1'
    print("Ensure that hosts myserver.com notmyserver.com and alsonotmyserver.com are in /etc/hosts and pointing to "+host);
    print("in uMatrix allow all to 1st party except XHR, and allow only XHR to notmyserver.com and alsonotmyserver.com which point to self aka "+host+" in your /etc/hosts")
    port=8080
    server_address = (host, port)
    print("listening on "+host+":"+str(port))
    httpd = HTTPServer(server_address, EchoServer)
    httpd.serve_forever()
