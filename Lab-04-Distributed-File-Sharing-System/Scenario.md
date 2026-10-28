## Lab scenario
A university has three departments: IT, Finance, and Administration. Each department stores files on its own server. Staff members need to upload and download files through a central client, even though the files are stored on different servers.
Students will build a simple distributed file-sharing system using Python.
<img width="770" height="412" alt="image" src="https://github.com/user-attachments/assets/8f1b40c9-46fa-4ccc-b454-63bc211012c5" />

## Lab objectives
By the end of the lab, students should be able to:
1. Explain how multiple servers cooperate in a distributed system.
2. Implement client-server communication using HTTP.
3. Store and retrieve files from different servers.
4. demonstrate what happens when one server becomes unavailable.
5. Explain the benefits and limitations of distributed storage.
3. Practical activities

Task 1 — Create the servers
Create three server instances running on ports 8001, 8002, and 8003. Each server must have its own storage directory.

Task 2 — Upload files
Upload lecture.txt to the IT server and budget.txt to the Finance server. Verify that each file is stored on the correct server.

Task 3 — Retrieve files
Use the client to request files from different servers and display their contents.

Task 4 — Simulate server failure
Stop Server 2 and attempt to retrieve budget.txt. Record the error and explain why the file may no longer be available.

Task 5 — Implement replication
Extend the system so that a copy of each file is stored on a second server. Stop the primary server and test whether the replicated file can still be retrieved.


## Questions for trainees
1. Why is this system considered distributed?
2. What is the role of the client, coordinator, and storage servers?
3. What happens when a server fails before replication is implemented?
4. How does replication improve availability?
5. What problems could occur if two users update the same file simultaneously?

## Expected deliverables
- Python source code for the client, coordinator, and three servers.
- Screenshots demonstrating file uploads and downloads.
- Evidence of the server-failure test.
- A short report explaining the architecture, results, and limitations.
## Important:
Run all three servers on one computer for the initial simulation. They are separate server processes, but not separate physical machines. For a more realistic distributed deployment, run them on different computers connected to the same network.

The code is designed to run on your Windows computer using separate Command Prompt or VS Code terminal windows.
1. Create the project folder
Create a folder named Distributed_File_Sharing with these four Python files:
<img width="771" height="202" alt="image" src="https://github.com/user-attachments/assets/64f6f7bb-17ac-45d2-aadf-af7a9b26ec9f" />

The storage servers will use ports 8001, 8002, and 8003. The coordinator will listen on port 8000.
2. Storage server — server.py
This program runs as one storage server. It can accept uploaded files, list stored files, and send files to clients.

3. Central coordinator — coordinator.py
The coordinator directs requests to the appropriate storage server according to the department selected by the user.
- IT → Server 1 (8001)
- Finance → Server 2 (8002)
- Administration → Server 3 (8003)

4. Client application — client.py
This is the program students use to interact with the distributed file system. It provides a menu to upload, list, and download files.

5. Run the lab on Windows
No external Python packages are required; all three programs use Python's standard library.

Open five separate terminals in your project folder.

First, navigate to the folder in each terminal:

If you saved the project somewhere else, use that folder's actual path.

Run these commands in order:
<img width="582" height="722" alt="image" src="https://github.com/user-attachments/assets/1fbefb6d-96ca-4293-9b17-b700a78149ac" />

Keep the first four terminals running while you use the client.
6. Test the system
1. Create a text file named lecture.txt containing Distributed Systems Lab.
2. Choose option 1 in the client and upload it to the IT department.
3. Choose option 2 and list files in the IT department.
4. Choose option 3 and download lecture.txt.
5. Open the downloaded copy inside the project's downloads folder and verify its contents.
The storage server creates directories such as storage_8001, storage_8002, and storage_8003 automatically.
7. Demonstrate a server failure
Stop the Finance server by pressing Ctrl+C in Terminal 2. Then try listing files or uploading a file to Finance.

The coordinator should return a 503 Service Unavailable error when it cannot contact that server. Restart it with:
python server.py 8002

Teaching note: This lab demonstrates distributed storage and communication, but it does not yet implement file replication. If a server fails, its files are unavailable through this system until that server returns. Replication can be added as an extension exercise.








