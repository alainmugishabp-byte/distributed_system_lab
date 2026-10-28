import json
import os
import secrets
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 8000
MAX_BYTES = 10 * 1024 * 1024
INTERNAL_TOKEN = "local-lab-token-change-me"

STORAGE_SERVERS = [
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
]

# DEMO ACCOUNTS ONLY. Do not use these credentials in a real deployment.
USERS = {
    "ituser": {"password": "it123", "department": "IT"},
    "financeuser": {"password": "fin123", "department": "FINANCE"},
    "adminuser": {"password": "admin123", "department": "ADMIN"},
}
SESSIONS = {}  # In-memory sessions; restarting the coordinator logs everyone out.


def valid_filename(name):
    return bool(name) and name not in (".", "..") and "/" not in name and "\\" not in name and len(name) <= 150


def request_json(url, method="GET", body=None, headers=None, timeout=2):
    req = urllib.request.Request(url, data=body, headers=headers or {}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
        return response.status, json.loads(raw.decode("utf-8")) if raw else {}


def storage_upload(server, key, content):
    headers = {
        "X-Internal-Token": INTERNAL_TOKEN,
        "X-Filename": key,
        "Content-Type": "application/octet-stream",
        "Content-Length": str(len(content)),
    }
    req = urllib.request.Request(server + "/upload", data=content, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=3) as response:
        return response.status


def get_user(handler):
    auth = handler.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    return SESSIONS.get(auth[7:])


class CoordinatorHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_bytes(self, content, filename):
        self.send_response(200)
        self.send_header("Content-Type", "application/octet-stream")
        self.send_header("Content-Disposition", "attachment; filename*=UTF-8''" + urllib.parse.quote(filename))
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def require_user(self):
        user = get_user(self)
        if not user:
            self.send_json(401, {"error": "Please log in again."})
            return None
        return user

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/":
            try:
                with open("client.html", "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except OSError:
                self.send_json(500, {"error": "client.html not found. Run coordinator.py from the project folder."})
            return

        if parsed.path == "/api/health":
            status = []
            for server in STORAGE_SERVERS:
                try:
                    _, data = request_json(server + "/health", timeout=1)
                    status.append({"server": server, "status": data.get("status", "unknown")})
                except Exception:
                    status.append({"server": server, "status": "unavailable"})
            self.send_json(200, {"coordinator": "running", "storage_servers": status})
            return

        if parsed.path == "/api/files":
            user = self.require_user()
            if not user:
                return
            department = query.get("department", [""])[0].upper()
            if department != user["department"]:
                self.send_json(403, {"error": "You can access only your own department."})
                return

            key_prefix = department + "__"
            found = set()
            available_servers = 0
            for server in STORAGE_SERVERS:
                try:
                    _, data = request_json(
                        server + "/files",
                        headers={"X-Internal-Token": INTERNAL_TOKEN},
                        timeout=2,
                    )
                    available_servers += 1
                    for key in data.get("files", []):
                        if key.startswith(key_prefix):
                            found.add(key[len(key_prefix):])
                except Exception:
                    pass

            if available_servers == 0:
                self.send_json(503, {"error": "All storage servers are unavailable."})
                return
            self.send_json(200, {"department": department, "files": sorted(found), "replica_servers_checked": available_servers})
            return

        if parsed.path == "/api/download":
            user = self.require_user()
            if not user:
                return
            department = query.get("department", [""])[0].upper()
            filename = query.get("filename", [""])[0]
            if department != user["department"]:
                self.send_json(403, {"error": "You can access only your own department."})
                return
            if not valid_filename(filename):
                self.send_json(400, {"error": "Invalid filename"})
                return

            key = department + "__" + filename
            for server in STORAGE_SERVERS:
                url = server + "/download/" + urllib.parse.quote(key)
                req = urllib.request.Request(url, headers={"X-Internal-Token": INTERNAL_TOKEN})
                try:
                    with urllib.request.urlopen(req, timeout=3) as response:
                        self.send_bytes(response.read(), filename)
                        return
                except Exception:
                    continue
            self.send_json(404, {"error": "File not found on any available storage server."})
            return

        self.send_json(404, {"error": "Unknown endpoint"})

    def do_POST(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/api/login":
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if size <= 0 or size > 5000:
                    self.send_json(400, {"error": "Invalid login request"})
                    return
                data = json.loads(self.rfile.read(size).decode("utf-8"))
            except Exception:
                self.send_json(400, {"error": "Send a valid JSON login request."})
                return

            username = str(data.get("username", ""))
            password = str(data.get("password", ""))
            account = USERS.get(username)
            if not account or not secrets.compare_digest(password, account["password"]):
                self.send_json(401, {"error": "Invalid username or password."})
                return

            token = secrets.token_urlsafe(32)
            SESSIONS[token] = {"username": username, "department": account["department"]}
            self.send_json(200, {"token": token, "username": username, "department": account["department"]})
            return

        if parsed.path == "/api/logout":
            auth = self.headers.get("Authorization", "")
            if auth.startswith("Bearer "):
                SESSIONS.pop(auth[7:], None)
            self.send_json(200, {"message": "Logged out"})
            return

        if parsed.path == "/api/upload":
            user = self.require_user()
            if not user:
                return

            department = query.get("department", [""])[0].upper()
            filename = query.get("filename", [""])[0]
            if department != user["department"]:
                self.send_json(403, {"error": "You can upload only to your own department."})
                return
            if not valid_filename(filename):
                self.send_json(400, {"error": "Invalid filename"})
                return

            try:
                size = int(self.headers.get("Content-Length", "0"))
            except ValueError:
                self.send_json(400, {"error": "Invalid content length"})
                return
            if size < 1 or size > MAX_BYTES:
                self.send_json(400, {"error": "File must be between 1 byte and 10 MB."})
                return

            content = self.rfile.read(size)
            if len(content) != size:
                self.send_json(400, {"error": "Incomplete upload"})
                return

            key = department + "__" + filename
            successful = []
            failed = []
            for server in STORAGE_SERVERS:
                try:
                    storage_upload(server, key, content)
                    successful.append(server)
                except Exception:
                    failed.append(server)

            if not successful:
                self.send_json(503, {"error": "Upload failed: all storage servers are unavailable."})
                return

            self.send_json(201, {
                "message": "Upload successful",
                "department": department,
                "filename": filename,
                "replicas_written": len(successful),
                "successful_servers": successful,
                "unavailable_servers": failed,
                "note": "The file is replicated to every storage server that was available."
            })
            return

        self.send_json(404, {"error": "Unknown endpoint"})

    def log_message(self, fmt, *args):
        print(f"[Coordinator] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), CoordinatorHandler)
    print(f"Coordinator running at http://{HOST}:{PORT}")
    print("Open http://127.0.0.1:8000 in your browser.")
    print("Demo accounts: ituser/it123, financeuser/fin123, adminuser/admin123")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCoordinator stopped.")
    finally:
        server.server_close()
