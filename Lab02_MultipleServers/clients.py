
import urllib.request
import json


SERVERS = [
    "http://localhost:8001",
    "http://localhost:8002",
    "http://localhost:8003"
]


def contact_server(server_url):

    print(f"\nConnecting to {server_url}")

    try:
        with urllib.request.urlopen(server_url, timeout=10) as response:
            data = response.read().decode("utf-8")
            result = json.loads(data)

            print(f"HTTP Status: {response.status}")
            print(f"Server:      {result['server']}")
            print(f"Port:        {result['port']}")
            print(f"Status:      {result['status']}")
            print(f"Message:     {result['message']}")
            print(f"Time:        {result['time']}")

    except Exception as error:
        print(f"ERROR: Could not contact {server_url}")
        print(f"Reason: {error}")


print("=======================================")
print("   DISTRIBUTED SYSTEMS CLIENT")
print("=======================================")

for server_url in SERVERS:
    contact_server(server_url)

print("\n=======================================")
print("Client finished contacting all servers.")
print("=======================================")
