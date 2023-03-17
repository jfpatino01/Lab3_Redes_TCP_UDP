import socket
import hashlib
import logging
import datetime

# Define host and port
HOST = 'localhost'
PORT = 8080

# Define filenames and paths
FILE_10MB = '10MB.txt'
FILE_100MB = '100MB.txt'

# Define hash function
HASH_FUNC = hashlib.sha256

# Set up logging
log_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-log.txt')
logging.basicConfig(filename=log_filename, level=logging.INFO)

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the specified host and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(25)

print('Server listening on port', PORT)

# Main loop
while True:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()

    logging.info(f'Connected by {client_address}')

    # Receive data from client
    data = client_socket.recv(1024).decode()

    # Process data here...
    if data == '10MB':
        filename = FILE_10MB
    elif data == '100MB':
        filename = FILE_100MB
    else:
        logging.warning(f'Invalid request from {client_address}')
        client_socket.sendall('Invalid request'.encode())
        client_socket.close()
        continue

    # Get file size
    file_size = os.path.getsize(filename)

    # Calculate hash of file
    with open(filename, 'rb') as f:
        file_data = f.read()
    file_hash = HASH_FUNC(file_data).hexdigest()

    # Send response to client and time the transfer
    start_time = datetime.datetime.now()
    client_socket.sendall(f'{file_hash}\n{file_data.decode()}'.encode())
    response = client_socket.recv(1024).decode()
    end_time = datetime.datetime.now()

    # Check if sending was accurate
    if response == 'ACK':
        logging.info(f'Sent {filename} ({file_size} bytes) to {client_address}. Transfer took {(end_time-start_time).total_seconds()} seconds.')
    else:
        logging.warning(f'Error sending {filename} ({file_size} bytes) to {client_address}. Transfer took {(end_time-start_time).total_seconds()} seconds.')

    # Close the connection
    client_socket.close()
