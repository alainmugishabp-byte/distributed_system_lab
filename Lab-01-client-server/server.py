#THIS IS FOR TEACHING PURPOSES


import socket

# Create a TCP socket
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Listen on the local computer, port 5000
server.bind(("127.0.0.1", 5000))
server.listen(5)

print("Server is running...")
print("Waiting for client connections...")

while True:
    connection, address = server.accept()

    print("Client connected:", address)

    message = connection.recv(1024).decode()
    print("Message received:", message)

    response = "Hello! Your request was received."
    connection.sendall(response.encode())

    connection.close()
