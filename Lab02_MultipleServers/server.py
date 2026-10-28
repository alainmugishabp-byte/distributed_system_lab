
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import socket
import sys
import time
from datetime import datetime


# ----------------------------------------
# Configuration
# ----------------------------------------

DEFAULT_PORT = 8001

if len(sys.argv) > 1:
    PORT = int(sys.argv[1])
else:
    PORT = DEFAULT_PORT

# Give each server a unique name
SERVER_NAME = f"Mugisha Server {PORT - 8000}"


# ----------------------------------------
# Request Handler
# ----------------------------------------

class RequestHandler(BaseHTTPRequestHandler):

    def send_json_response(self, data, status_code=200):
        response = json.dumps(data).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path == "/":
            response = {
                "message": "Hello from a distributed server!",
                "server": SERVER_NAME,
                "port": PORT,
                "time": datetime.now().isoformat(),
                "status": "running"
            }
            self.send_json_response(response)

        elif self.path == "/hello":
            response = {
                "message": "Hello, client!",
                "server": SERVER_NAME,
                "port": PORT
            }
            self.send_json_response(response)

        elif self.path == "/health":
            response = {
                "status": "healthy",
                "server": SERVER_NAME,
                "port": PORT
            }
            self.send_json_response(response)

        elif self.path == "/slow":
            time.sleep(5)

            response = {
                "message": "This server intentionally responds slowly.",
                "server": SERVER_NAME,
                "port": PORT
            }
            self.send_json_response(response)

        else:
            response = {
                "error": "Endpoint not found",
                "server": SERVER_NAME
            }
            self.send_json_response(response, status_code=404)

    def log_message(self, format, *args):
        print(
            f"[{SERVER_NAME}] "
            f"{self.address_string()} - "
            f"{format % args}"
        )


# ----------------------------------------
# Start Server
# ----------------------------------------

server = HTTPServer(("localhost", PORT), RequestHandler)

print("=======================================")
print("   DISTRIBUTED SYSTEMS SERVER")
print("=======================================")
print(f"Server Name: {SERVER_NAME}")
print(f"Port:        {PORT}")
print(f"URL:         http://localhost:{PORT}")
print("Status:      Running")
print("=======================================")
print("Press CTRL+C to stop the server.")

try:
    server.serve_forever()

except KeyboardInterrupt:
    print(f"\n{SERVER_NAME} is shutting down...")

finally:
    server.server_close()
