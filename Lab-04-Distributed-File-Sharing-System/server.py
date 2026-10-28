import os
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote

HOST = "localhost"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8001

SERVER_NAME = f"Storage-Server-{PORT}"
STORAGE_DIR = f"storage_{PORT}"

os.makedirs(STORAGE_DIR, exist_ok=True)


class StorageHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/health":
            self.send_json(200, {
                "server": SERVER_NAME,
                "port": PORT,
                "status": "healthy"
            })

        elif path == "/files":
            files = os.listdir(STORAGE_DIR)
            self.send_json(200, {
                "server": SERVER_NAME,
                "files": files
            })

        elif path.startswith("/download/"):
            filename = unquote(path[len("/download/"):])

            # Only allow a simple filename, not a directory path.
            if not filename or filename in (".", "..") or "/" in filename or "\\" in filename:
                self.send_json(400, {"error": "Invalid filename"})
                return

            filepath = os.path.join(STORAGE_DIR, filename)

            if not os.path.isfile(filepath):
                self.send_json(404, {"error": "File not found"})
                return

            with open(filepath, "rb") as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header(
                "Content-Disposition",
                f'attachment; filename="{filename}"'
            )
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)

        else:
            self.send_json(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/upload":
            self.send_json(404, {"error": "Unknown endpoint"})
            return

        filename = self.headers.get("X-Filename", "")

        if (
            not filename
            or filename in (".", "..")
            or "/" in filename
            or "\\" in filename
        ):
            self.send_json(400, {"error": "Invalid filename"})
            return

        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"error": "Invalid file size"})
            return

        if size <= 0 or size > 10 * 1024 * 1024:
            self.send_json(400, {
                "error": "File must be between 1 byte and 10 MB"
            })
            return

        content = self.rfile.read(size)
        filepath = os.path.join(STORAGE_DIR, filename)

        with open(filepath, "wb") as file:
            file.write(content)

        self.send_json(201, {
            "message": "File uploaded successfully",
            "server": SERVER_NAME,
            "filename": filename,
            "size": len(content)
        })

    def log_message(self, format, *args):
        print(f"[{SERVER_NAME}] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), StorageHandler)
    print(f"{SERVER_NAME} running at http://{HOST}:{PORT}")
    print(f"Storage directory: {os.path.abspath(STORAGE_DIR)}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{SERVER_NAME} stopped.")
    finally:
        server.server_close()
