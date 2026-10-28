import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode

HOST = "localhost"
PORT = 8000

SERVERS = {
    "IT": "http://localhost:8001",
    "FINANCE": "http://localhost:8002",
    "ADMIN": "http://localhost:8003",
}


class CoordinatorHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def get_server(self, query):
        department = query.get("department", [""])[0].upper()
        return SERVERS.get(department)

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/health":
            self.send_json(200, {
                "coordinator": "running",
                "storage_servers": SERVERS
            })
            return

        server = self.get_server(query)

        if not server:
            self.send_json(400, {
                "error": "Choose IT, FINANCE, or ADMIN"
            })
            return

        if parsed.path == "/files":
            target = server + "/files"

        elif parsed.path == "/download":
            filename = query.get("filename", [""])[0]

            if (
                not filename
                or filename in (".", "..")
                or "/" in filename
                or "\\" in filename
            ):
                self.send_json(400, {"error": "Invalid filename"})
                return

            target = server + "/download/" + urllib.parse.quote(filename)

        else:
            self.send_json(404, {"error": "Unknown endpoint"})
            return

        try:
            with urllib.request.urlopen(target, timeout=5) as response:
                content = response.read()

                if parsed.path == "/download":
                    self.send_response(response.status)
                    self.send_header(
                        "Content-Type", "application/octet-stream"
                    )
                    self.send_header(
                        "Content-Length", str(len(content))
                    )
                    self.end_headers()
                    self.wfile.write(content)
                else:
                    self.send_response(response.status)
                    self.send_header(
                        "Content-Type", "application/json"
                    )
                    self.send_header(
                        "Content-Length", str(len(content))
                    )
                    self.end_headers()
                    self.wfile.write(content)

        except urllib.error.HTTPError as error:
            self.send_json(error.code, {
                "error": "Storage server returned an error",
                "details": error.read().decode(
                    "utf-8", errors="replace"
                )
            })

        except (urllib.error.URLError, TimeoutError, OSError) as error:
            self.send_json(503, {
                "error": "Storage server unavailable",
                "details": str(error)
            })

    def do_POST(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path != "/upload":
            self.send_json(404, {"error": "Unknown endpoint"})
            return

        server = self.get_server(query)
        filename = query.get("filename", [""])[0]

        if not server:
            self.send_json(400, {
                "error": "Choose IT, FINANCE, or ADMIN"
            })
            return

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

        request = urllib.request.Request(
            server + "/upload",
            data=content,
            headers={
                "Content-Type": "application/octet-stream",
                "X-Filename": filename,
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                result = json.loads(response.read().decode("utf-8"))
                self.send_json(response.status, result)

        except urllib.error.HTTPError as error:
            self.send_json(error.code, {
                "error": error.read().decode(
                    "utf-8", errors="replace"
                )
            })

        except (urllib.error.URLError, TimeoutError, OSError) as error:
            self.send_json(503, {
                "error": "Storage server unavailable",
                "details": str(error)
            })

    def log_message(self, format, *args):
        print(f"[Coordinator] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CoordinatorHandler)
    print(f"Coordinator running at http://{HOST}:{PORT}")
    print("Departments: IT, FINANCE, ADMIN")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCoordinator stopped.")
    finally:
        server.server_close()
