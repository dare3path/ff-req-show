#!/usr/bin/python3
import http.server
import socketserver
import time

# a slow server (made by grok3) which replies in 5 sec, for bug: https://bugzilla.mozilla.org/show_bug.cgi?id=1557795
class DelayedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve a page with a button to trigger POST
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        html = """
        <html>
            <body>
                <h1>Delayed POST Test</h1>
                <input type="text" id="message" value="Test message">
                <button onclick="sendPost()">Send POST Request</button>
                <div id="response"></div>
                
                <script>
                    async function sendPost() {
                        const message = document.getElementById('message').value;
                        const responseDiv = document.getElementById('response');
                        responseDiv.innerHTML = 'Waiting...';
                        
                        const response = await fetch('/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'message=' + encodeURIComponent(message)
                        });
                        
                        const text = await response.text();
                        responseDiv.innerHTML = text;
                    }
                </script>
            </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        # Delay for 5 seconds
        time.sleep(5)
        
        # Get the POST data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        
        # Send response (just the payload for simplicity)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = f"Received payload: {post_data}"
        self.wfile.write(response.encode())

# Set up and run the server
PORT = 8001
Handler = DelayedHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
