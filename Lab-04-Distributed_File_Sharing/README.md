# Distributed File Sharing System Using Python

A practical **Distributed Systems Management** project demonstrating client-server communication, distributed storage, file replication, server-failure handling, and basic authentication using Python and a web-based interface.

## 📌 Project Overview

The Distributed File Sharing System allows users to upload, list, and download files through a browser-based application. A central coordinator manages client requests and communicates with multiple storage servers.

Files are replicated across available storage servers to improve data availability when an individual storage server becomes unavailable.

This project is designed for educational purposes to demonstrate fundamental concepts of distributed systems through a practical, hands-on implementation.

## 🎯 Objectives

- Understand distributed client-server architecture.
- Implement communication between a coordinator and multiple storage servers.
- Develop a browser-based file-sharing interface.
- Distribute and replicate files across multiple storage servers.
- Demonstrate basic user authentication and departmental access control.
- Test server availability and observe failure-handling behavior.
- Explore the benefits and limitations of distributed storage.

## 🏗️ System Architecture

```text
                 Web Browser Client
                         |
                         v
               Coordinator Server
                  Port 8000
                         |
            +------------+------------+
            |            |            |
            v            v            v
       IT Storage    Finance       Administration
       Port 8001     Port 8002      Port 8003
            |            |            |
            +------ File Replication-+
```

All components can run as separate processes on one computer for demonstration. They can also be adapted for deployment across separate computers.

## ✨ Key Features

- **File upload:** Upload files through a browser.
- **File listing:** View files belonging to the authenticated user's department.
- **File download:** Retrieve stored files through the coordinator.
- **Distributed storage:** Use three independent storage-server processes.
- **File replication:** Write uploaded files to all storage servers that are available.
- **Failure handling:** Continue uploading and retrieving replicated files when at least one storage server remains available.
- **Basic authentication:** Sign in using department-specific demo accounts.
- **Access control:** Restrict users to their assigned department.
- **Server health checks:** Check which storage servers are responding.
- **File size limit:** Accept non-empty files up to 10 MB.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Server-side application and HTTP communication |
| HTML | Web interface structure |
| CSS | User-interface styling |
| JavaScript | Browser interactions and API requests |
| Python HTTP Server | Coordinator and storage-server endpoints |
| HTTP/JSON | Client-server communication and API responses |

No third-party Python packages are required for the current implementation.

## 📂 Project Structure

```text
Distributed_File_Sharing/
├── coordinator.py
├── storage_server.py
├── client.html
├── start_servers.bat
├── README.md
├── storage_8001/
├── storage_8002/
└── storage_8003/
```

- `coordinator.py` — handles authentication, routing, replication, and downloads.
- `storage_server.py` — implements the storage-server API.
- `client.html` — provides the browser-based interface.
- `start_servers.bat` — starts the three storage servers.
- `storage_8001/`, `storage_8002/`, and `storage_8003/` — contain files stored by the respective servers.

## ⚙️ Requirements

- Windows 10/11 or a compatible operating system.
- Python 3 installed and accessible from the terminal.
- A modern web browser.
- A code editor such as Visual Studio Code (optional).

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Distributed_File_Sharing
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual URL of your GitHub repository.

Alternatively, download the repository as a ZIP file and extract it.

### 2. Start the storage servers

On Windows, double-click:

```text
start_servers.bat
```

This opens separate terminal windows for the storage servers on ports `8001`, `8002`, and `8003`.

### 3. Start the coordinator

Open a new terminal in the project directory and run:

```bash
python coordinator.py
```

### 4. Open the web application

Navigate to:

```text
http://127.0.0.1:8000
```

Keep the coordinator and storage-server processes running while using the application.

## 🔐 Demo Accounts

| Department | Username | Password |
|---|---|---|
| IT | `ituser` | `it123` |
| Finance | `financeuser` | `fin123` |
| Administration | `adminuser` | `admin123` |

**Security notice:** These are demonstration credentials only. Never use them for real accounts or confidential information.

## 🧪 Practical Testing

### Test 1: File Upload

1. Sign in using the IT demo account.
2. Select a small, non-empty file.
3. Click **Upload and replicate**.
4. Observe the number of successful replicas.

**Expected result:** The file is stored on each storage server that is available at upload time.

### Test 2: File Listing and Download

1. Refresh the file list.
2. Locate the uploaded file.
3. Click **Download**.

**Expected result:** The application retrieves a copy from an available storage server.

### Test 3: Storage Server Failure

1. Stop one storage server using `Ctrl+C` in its terminal.
2. Upload another file.
3. Observe the available and unavailable servers.
4. Download a file that was replicated before the failure.

**Expected result:** The upload can succeed using the remaining available servers, and existing replicas may allow downloads to continue.

### Test 4: Departmental Access Control

1. Sign in as `ituser`.
2. Attempt to access the Finance department through the application's API.
3. Observe the response.

**Expected result:** The coordinator rejects access to a department that does not match the authenticated user's assigned department.

### Test 5: Server Health

Click **Check server status** in the application.

**Expected result:** The interface reports the coordinator's status and indicates which storage servers are healthy or unavailable.

## 📚 Distributed Systems Concepts Demonstrated

- Client-server architecture
- Distributed storage
- HTTP-based communication
- Service coordination and request routing
- Data replication
- Fault tolerance and availability
- Failure detection
- Authentication and authorization
- Single points of failure
- Distributed-system testing

## ⚠️ Current Limitations

- The coordinator is a single point of failure.
- Replicas are written only to servers available during an upload.
- Automatic replica repair and synchronization are not implemented.
- Demo credentials are hardcoded and passwords are not securely hashed.
- The application uses HTTP rather than HTTPS.
- Storage servers are intended for local educational testing and should not be exposed directly to the public internet.
- File uploads are limited to 10 MB.
- There is no persistent database for users or sessions.

## 🔮 Future Improvements

- Implement secure password hashing and stronger session management.
- Add HTTPS and secure configuration management.
- Introduce automatic replica repair and synchronization.
- Implement file checksums for integrity verification.
- Add a database for user accounts and file metadata.
- Introduce logging, monitoring, and audit trails.
- Deploy storage servers on separate machines or virtual machines.
- Add load balancing and coordinator redundancy.

## 🎓 Educational Use

This project can be used as a practical laboratory exercise for students studying Distributed Systems Management, Computer Networks, and Software Engineering.

Students can extend the application, evaluate its behavior under failure conditions, and document their observations in a laboratory report.

## 👨‍💻 Author

**Alain Mugisha**

IT Support Specialist | Network & Security Engineer | Cybersecurity Professional | Cisco Academy Instructor

## 📄 License

This project is intended for educational and demonstration purposes. Add an open-source license, such as the MIT License, if you want others to reuse and modify the code under its terms.
