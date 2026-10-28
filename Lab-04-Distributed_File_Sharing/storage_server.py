import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

HOST = "127.0.0.1"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001
STORAGE_DIR = f"storage_{PORT}"
INTERNAL_TOKEN = "local-lab-token-change-me"
MAX_BYTES = 10 * 1024 * 1024

os.makedirs(STORAGE_DIR, exist_ok=True)


def valid_name(name):
    return bool(name) and name not in (".", "..") and "/" not in name and "\\" not in name and len(name) <= 180


class StorageHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def authorized(self):
        return self.headers.get("X-Internal-Token") == INTERNAL_TOKEN

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self.send_json(200, {"server": f"Storage-{PORT}", "status": "healthy", "port": PORT})
            return

        if not self.authorized():
            self.send_json(401, {"error": "Unauthorized internal request"})
            return

        if path == "/files":
            self.send_json(200, {"server": f"Storage-{PORT}", "files": sorted(os.listdir(STORAGE_DIR))})
            return

        if path.startswith("/download/"):
            key = unquote(path[len("/download/"):])
            if not valid_name(key):
                self.send_json(400, {"error": "Invalid storage key"})
                return
            filepath = os.path.join(STORAGE_DIR, key)
            if not os.path.isfile(filepath):
                self.send_json(404, {"error": "File not found"})
                return
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_json(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        if urlparse(self.path).path != "/upload":
            self.send_json(404, {"error": "Unknown endpoint"})
            return
        if not self.authorized():
            self.send_json(401, {"error": "Unauthorized internal request"})
            return

        key = self.headers.get("X-Filename", "")
        if not valid_name(key):
            self.send_json(400, {"error": "Invalid storage key"})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid content length"})
            return

        if size < 1 or size > MAX_BYTES:
            self.send_json(400, {"error": "File must be between 1 byte and 10 MB"})
            return

        content = self.rfile.read(size)
        if len(content) != size:
            self.send_json(400, {"error": "Incomplete upload"})
            return

        with open(os.path.join(STORAGE_DIR, key), "wb") as f:
            f.write(content)

        self.send_json(201, {"message": "Stored", "server": f"Storage-{PORT}", "key": key, "size": len(content)})

    def log_message(self, fmt, *args):
        print(f"[Storage {PORT}] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), StorageHandler)
    print(f"Storage server running at http://{HOST}:{PORT}")
    print(f"Files are stored in: {os.path.abspath(STORAGE_DIR)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\nStorage server {PORT} stopped.")
    finally:
        server.server_close()
