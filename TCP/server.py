import socket
import hashlib
import os
import datetime

HOST = '192.168.64.10'
PORT = 5555
FILES = {
    '10MB.txt': 10485760,
    '100MB.txt': 104857600,
}
LOG_FILE_NAME_FORMAT = '%Y-%m-%d-%H-%M-%S-log.txt'


def handle_client(conn, addr, file_name):
    with open(file_name, 'rb') as f:
        data = f.read()
        hash_obj = hashlib.sha256(data)
        hash_hex = hash_obj.hexdigest()
        conn.sendall(data)
        conn.sendall(hash_hex.encode('utf-8'))
        ack = conn.recv(1024)
        if ack == hash_hex.encode('utf-8'):
            print(f'Successfully sent {file_name} to {addr}')
            return True
        else:
            print(f'Error sending {file_name} to {addr}')
            return False


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(25)
    print(f'Server listening on {HOST}:{PORT}')
    
    while True:
        conn, addr = server_socket.accept()
        print(f'Connected by {addr}')
        
        if len(os.listdir()) == len(FILES):
            conn.sendall(b'Server is full')
            conn.close()
            continue
        
        file_choice = conn.recv(1024).decode('utf-8')
        if file_choice not in FILES:
            conn.sendall(b'Invalid file choice')
            conn.close()
            continue
        
        file_size = FILES[file_choice]
        conn.sendall(str(file_size).encode('utf-8'))
        log_file_name = datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT)
        with open(log_file_name, 'a') as log_file:
            log_file.write(f'{addr} requested {file_choice} of size {file_size}\n')
        
        if handle_client(conn, addr, file_choice):
            with open(log_file_name, 'a') as log_file:
                log_file.write(f'Successfully sent {file_choice} of size {file_size} to {addr}\n')
        else:
            with open(log_file_name, 'a') as log_file:
                log_file.write(f'Error sending {file_choice} of size {file_size} to {addr}\n')
        
        conn.close()


if __name__ == '__main__':
    main()
