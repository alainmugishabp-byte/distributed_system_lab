Step 1: Understand the result
<img width="846" height="185" alt="image" src="https://github.com/user-attachments/assets/609c5d73-298a-4e41-ba29-ed0abe5fc107" />

Your server code is designed to accept a port number when you start it. If you run it without a port argument, it uses port 8001 by default.
Step 2: Start Server 2
Open a second PowerShell or CMD window.

Navigate to your lab folder:

Then run:
python server.py 8002

You should see something like:
Distributed Systems Server
Server: MUGISHA
Port:   8002
URL:    http://localhost:8002
Press CTRL+C to stop the server.

Leave this window open.
Step 3: Start Server 3
Open a third PowerShell or CMD window and run the same folder command:

Then run:
python server.py 8003

You should see:
Distributed Systems Server
Server: MUGISHA
Port:   8003
URL:    http://localhost:8003
Press CTRL+C to stop the server.

Leave this window open too.
Step 4: Keep Server 1 running
Your original Server 1 should still be running in its first terminal window on port 8001.

You should now have three terminal windows:
<img width="962" height="442" alt="image" src="https://github.com/user-attachments/assets/52a52a00-26db-4429-a2cb-b522094e3246" />

Step 5: Run your client again
Open another terminal window, navigate to the folder, and run your client file. For example, if it is named client.py:

python client.py

Distributed Systems Client

Connecting to http://localhost:8001
Status: 200
Server: MUGISHA
Port:   8001
Status: running

Connecting to http://localhost:8002
Status: 200
Server: MUGISHA
Port:   8002
Status: running

Connecting to http://localhost:8003
Status: 200
Server: MUGISHA
Port:   8003
Status: running

Your hostname may differ, but all three ports should respond.

Important: Your current setup demonstrates three server processes on one computer. They share the same hostname, but listen on different ports. This is a useful distributed-systems simulation.
