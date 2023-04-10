import socket
import hashlib
import os
import datetime

HOST = '127.0.0.1'
PORT = 5555
FILES = {
    '250MB.txt': 262144000,
    '100MB.txt': 104857600,
}
LOG_FILE_NAME_FORMAT = '%Y-%m-%d-%H-%M-Server-log.txt'
connections = []
MAX_CONNECTIONS = 25


def handle_client(conn, addr, file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
        hash_obj = hashlib.sha256(data)
        hash_hex = hash_obj.hexdigest()

    chunk_size = 1024 * 1024 * 10  #10 MB
    with open(file_name, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            conn.sendall(chunk)

        ack = conn.recv(1024)
        if ack == hash_hex.encode('utf-8'):
            conn.sendall('Success'.encode('utf-8'))
            print(f'Successfully sent {file_name} to {addr}')
            return True
        else:
            print(f'Error sending {file_name} to {addr}')
            conn.sendall('Failure'.encode('utf-8'))
            return False


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(25)
    print(f'Server listening on {HOST}:{PORT}')
    connection_counter = 0

    while True:
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')
        

        if len(connections) < MAX_CONNECTIONS:
            connections.append(conn)
            connection_counter += 1
        if connection_counter < MAX_CONNECTIONS:
            print('waiting')
        else:
            print('=====AHORA COMENZAMOS A PROCESAR=====')
            for conn in connections:
                file_choice = conn.recv(1024).decode('utf-8')
                file_size = FILES[file_choice]
                conn.sendall(str(file_size).encode('utf-8'))
                log_file_name = datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT)
                with open(log_file_name, 'a') as log_file:
                    log_file.write(f'{addr} requested {file_choice} of size {file_size}\n')
                    if handle_client(conn, addr, file_choice):
                        log_file.write(f'Successfully sent {file_choice} of size {file_size} to {addr}\n')
                    else:
                        log_file.write(f'Error sending {file_choice} of size {file_size} to {addr}\n')
                connection_counter -= 1
                conn.close()


if __name__ == '__main__':
    main()
