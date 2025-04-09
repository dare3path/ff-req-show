#!/usr/bin/python3
import http.server
import socketserver
import time

class DelayedHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve a page with two buttons
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        html = """
        <html>
            <body>
                <h1>POST Request Test</h1>
                <input type="text" id="message" value="Test message">
                <button onclick="sendDelayed()">Send Delayed POST (5s)</button>
                <button onclick="sendFast()">Send Fast POST</button>
                <div id="response"></div>
                
                <script>
                    async function sendDelayed() {
                        const message = document.getElementById('message').value;
                        const responseDiv = document.getElementById('response');
                        responseDiv.innerHTML = 'Waiting 5 seconds...';
                        
                        const response = await fetch('/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'message=\x02' + encodeURIComponent(message)
                        });
                        
                        const text = await response.text();
                        responseDiv.innerHTML = text;
                    }
                    
                    async function sendFast() {
                        const message = document.getElementById('message').value;
                        const responseDiv = document.getElementById('response');
                        responseDiv.innerHTML = 'Sending fast...';
                        
                        const response = await fetch('/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: 'fastmsg=\x03' + encodeURIComponent(message)
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
        # Get the POST data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        
        # Check if it's a delayed or fast request
        if post_data.startswith('message='):
            # Delayed response (5 seconds)
            time.sleep(5)
        # else it's fastmsg=, so no delay
        
        # Send response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = f"Received payload: {post_data}"
        self.wfile.write(response.encode())

# Set up and run the server on port 8001
PORT = 8001
Handler = DelayedHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
