import socket
import hashlib
import os
import datetime

# Set up the TCP connection
HOST = '192.168.64.10' # Replace with the IP address of your server
PORT = 5555 # Replace with the port number of your server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Set up the folder for received files
if not os.path.exists('ArchivosRecibidos'):
    os.makedirs('ArchivosRecibidos')

# Set up the log file
log_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-log.txt')
log_file = open(log_filename, 'w')

# Generate random requests for files
for i in range(25):
    
    # Send the request to the server
    request = i % 2
    print(request)
    client_socket.send(request.encode('utf-8'))

    # Receive the file from the server
    file_size = int(client_socket.recv(1024).decode())
    file_data = b''
    while len(file_data) < file_size:
        data = client_socket.recv(1024)
        file_data += data

    # Check the integrity of the received file
    received_hash = hashlib.md5(file_data).hexdigest()
    expected_hash = client_socket.recv(1024).decode()
    is_valid = received_hash == expected_hash

    # Save the file and rename it
    filename = f"{i+1}-Prueba-{filename}"
    with open(os.path.join('ArchivosRecibidos', filename), 'wb') as f:
        f.write(file_data)

    # Log the information about the transfer
    log_line = f"{filename}\t{file_size}\t{client_socket.getpeername()}\t{is_valid}\n"
    log_file.write(log_line)

# Close the log file and the socket
log_file.close()
client_socket.close()
