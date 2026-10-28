These three Python programs are for the next stage of your Distributed Systems Management lab. They introduce load balancing and health monitoring on top of your three-server setup.

In simple terms, instead of the client contacting each server directly, the client sends requests to a load balancer, which distributes them among available servers.
1. How the system works
<img width="962" height="532" alt="image" src="https://github.com/user-attachments/assets/0a18d5d1-d143-49ae-aa02-ffe903f578f4" />

2. What each code does
Code 1: Client
The first program is the client. It sends six HTTP requests to:
LOAD_BALANCER = "http://localhost:8000"

It uses urllib.request to make HTTP requests and json to read the JSON responses. The loop:
for request_number in range(1, 7):

sends six requests, while:
time.sleep(1)

waits one second between requests.

Why? To demonstrate how multiple requests can be distributed across several servers without the client needing to know which backend server handles each request.
Code 2: Load balancer
The second program is the load balancer, listening on port 8000.

It has three important responsibilities:
- Health checking: check_server_health() contacts each backend's /health endpoint to determine whether it responds with HTTP status 200.
- Round-robin distribution: it uses current_server to choose the next server from the healthy-server list.
- Request forwarding: it sends the client's request to the chosen backend and returns that server's response to the client.
The health checker runs in a background thread and checks every three seconds:

HEALTH_CHECK_INTERVAL = 3

If no healthy servers are available, the load balancer returns HTTP 503 Service Unavailable.

Why? To improve availability and distribute incoming requests instead of relying on a single backend.
Code 3: Backend server
The third program is the backend HTTP server. You run it multiple times using different port numbers.

For example:
<img width="991" height="172" alt="image" src="https://github.com/user-attachments/assets/c203fa36-3406-4ec2-81c4-ef12dff515c3" />

The code sets the server's identity based on its port:
SERVER_NAME = f"Server-{PORT}"

So the responses identify Server-8001, Server-8002, and Server-8003.

It also provides two endpoints:
<img width="652" height="132" alt="image" src="https://github.com/user-attachments/assets/66ea60c6-f707-416b-9eed-131296691021" />

Why? The load balancer needs a health endpoint to determine which backend servers are responding.
3. How the three programs work together
When the client sends six requests, the load balancer should distribute them approximately like this, assuming all three servers are healthy and the health list remains unchanged:

<img width="742" height="336" alt="image" src="https://github.com/user-attachments/assets/bfb0ffe5-b4e0-41c7-a14d-221097393958" />

The actual sequence can differ if the healthy-server list changes. The first server in the list is not guaranteed to be port 8001 if the health checker has not completed its initial check.
4. How to run the lab
Save the three programs in your lab folder using these filenames:
- client.py
- load_balancer.py
- server.py

Open five terminal windows. Run the following commands in the same folder.
<img width="582" height="727" alt="image" src="https://github.com/user-attachments/assets/cf04f7f7-8336-4206-89ed-d1e6fc651b5e" />

Start the backend servers first, then the load balancer, and finally the client. Keep the server and load-balancer terminals open.
5. What students can learn from this lab
1. The difference between a client, backend server and load balancer.
2. How HTTP requests and JSON responses work.
3. How round-robin load balancing distributes requests.
4. How health checks identify unavailable servers.
5. How a system responds when all backend servers become unavailable.

Important limitation: this is a teaching implementation, not a production-ready load balancer. It uses Python's single-threaded HTTPServer, and if a selected server fails after the last health check, the current request can fail instead of automatically retrying another backend. Also, all servers currently run on one physical computer, so this demonstrates distributed-system concepts without providing physical server redundancy.






