import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from middleware import Middleware

middleware = Middleware()

class PingPongHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        start_time = time.time()
        if self.path == "/ping":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"message": "pong"}')
            self.log_message("Handled /ping request successfully without Flask.")
            success = True
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid endpoint"}')
            self.log_message("Handled invalid request.")
            success = False

        # Process metrics
        middleware.process_request(self, start_time)  # Pass handler

def start_http_server(host='0.0.0.0', port=3001):
    server_address = ('', port)
    httpd = HTTPServer(server_address, PingPongHTTPHandler)
    print(f"HTTP server running on port {port}")
    httpd.serve_forever()
