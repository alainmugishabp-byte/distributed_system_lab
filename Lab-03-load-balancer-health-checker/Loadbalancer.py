from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import threading
import time


SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]

HEALTH_CHECK_INTERVAL = 3

healthy_servers = []

current_server = 0

lock = threading.Lock()


def check_server_health(server):

    try:

        with urllib.request.urlopen(
            f"{server}/health",
            timeout=1
        ) as response:

            return response.status == 200

    except Exception:

        return False


def health_checker():

    global healthy_servers

    while True:

        new_healthy_servers = []

        print("\n[Health Check] Checking servers...")

        for server in SERVERS:

            if check_server_health(server):

                print(f"[Health Check] ✓ {server} is healthy")

                new_healthy_servers.append(server)

            else:

                print(f"[Health Check] ✗ {server} is unhealthy")

        with lock:

            healthy_servers = new_healthy_servers

        time.sleep(HEALTH_CHECK_INTERVAL)


class LoadBalancerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        global current_server

        with lock:

            available_servers = healthy_servers.copy()

        if not available_servers:

            self.send_response(503)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            message = b'{"error": "No healthy servers available"}'

            self.wfile.write(message)

            print(
                "[Load Balancer] "
                "No healthy servers available"
            )

            return

        server = available_servers[
            current_server % len(available_servers)
        ]

        current_server += 1

        print(
            f"[Load Balancer] "
            f"Forwarding request to {server}"
        )

        try:

            with urllib.request.urlopen(
                server + self.path,
                timeout=2
            ) as response:

                data = response.read()

                self.send_response(response.status)

                self.send_header(
                    "Content-Type",
                    response.headers.get(
                        "Content-Type",
                        "application/json"
                    )
                )

                self.send_header(
                    "Content-Length",
                    str(len(data))
                )

                self.end_headers()

                self.wfile.write(data)

        except Exception as error:

            print(
                f"[Load Balancer] "
                f"Request failed: {error}"
            )

            self.send_response(503)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            message = b'{"error": "Backend server unavailable"}'

            self.wfile.write(message)

    def log_message(self, format, *args):

        print(
            f"[Load Balancer] "
            f"{format % args}"
        )


def start_health_checker():

    thread = threading.Thread(
        target=health_checker,
        daemon=True
    )

    thread.start()


server = HTTPServer(
    ("localhost", 8000),
    LoadBalancerHandler
)


print("---------------------------------------")
print("Health-Aware Load Balancer")
print("---------------------------------------")
print("Port: 8000")
print("URL:  http://localhost:8000")
print("---------------------------------------")
print("Backend servers:")

for backend in SERVERS:
    print(f"  - {backend}")

print("---------------------------------------")
print(
    f"Health checks every "
    f"{HEALTH_CHECK_INTERVAL} seconds"
)
print("---------------------------------------")


start_health_checker()


try:

    server.serve_forever()

except KeyboardInterrupt:

    print("\nLoad balancer shutting down...")
    server.server_close()
