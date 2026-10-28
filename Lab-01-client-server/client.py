import socket

# Create a TCP socket
client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Connect to the server
server_ip = input("Enter server IP address: ")

client.connect((server_ip, 5000))

print("Connected to the server.")

# Send a message
message = input("Enter your message: ")
client.sendall(message.encode())

# Receive the response
response = client.recv(1024).decode()

print("Server response:", response)

# Close the connection
client.close()

print("Connection closed.")


#THIS IS FOR TEACHING PURPOSES
#Lecturer. MUGISHA Alain
