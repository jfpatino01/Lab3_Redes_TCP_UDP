import socket
import hashlib
import os
import random
import string
import datetime
import logging

# Define host and port
HOST = 'localhost'
PORT = 8080

# Define filenames and paths
FILE_10MB = '10MB.txt'
FILE_100MB = '100MB.txt'

# Define hash function
HASH_FUNC = hashlib.sha256

# Create a directory to store received files
if not os.path.exists('ArchivosRecibidos'):
    os.makedirs('ArchivosRecibidos')

# Set up logging
log_filename = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S-log.txt')
logging.basicConfig(filename=log_filename, level=logging.INFO)

# Main loop to generate 25 users and randomly request files
for i in range(25):
    # Generate a random request for a file
    if random.randint(0, 1) == 0:
        filename = FILE_10MB
    else:
        filename = FILE_100MB

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Get file hash
    with open(filename, 'rb') as f:
        file_data = f.read()
    file_hash = HASH_FUNC(file_data).hexdigest()

    # Send request to server and time the transfer
    start_time = datetime.datetime.now()
    client_socket.sendall(filename.encode())
    response = client_socket.recv(1024).decode().split('\n')
    end_time = datetime.datetime.now()

    # Check file integrity
    if response[0] == file_hash:
        logging.info(f'Received {filename} ({len(response[1])} bytes) from server. Transfer took {(end_time-start_time).total_seconds()} seconds.')

        # Save received file with a unique name
        file_number = i + 1
        connection_number = random.randint(1, 25)
        new_filename = f'{file_number}-Prueba-{connection_number}.txt'
        with open(os.path.join('ArchivosRecibidos', new_filename), 'w') as f:
            f.write(response[1])
    else:
        logging.warning(f'Error receiving {filename} from server. Transfer took {(end_time-start_time).total_seconds()} seconds.')

    # Send acknowledgement to server
    client_socket.sendall('ACK'.encode())

    # Close the connection
    client_socket.close()
