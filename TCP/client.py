import socket
import hashlib
import os
import datetime

HOST = '127.0.0.1'
PORT = 5555
FILES = [
    '10MB.txt',
    '100MB.txt',
]
LOG_FILE_NAME_FORMAT = '%Y-%m-%d-%H-%M-%S-log.txt'
ARCHIVE_FOLDER_NAME = 'ArchivosRecibidos'


def receive_file(conn, file_size, file_name):
    data_received = 0
    with open(os.path.join(ARCHIVE_FOLDER_NAME, file_name), 'wb') as f:
        while data_received < file_size:
            data = conn.recv(1024)
            if not data:
                break
            f.write(data)
            data_received += len(data)
        f.flush()
        hash_hex = hashlib.sha256(open(os.path.join(ARCHIVE_FOLDER_NAME, file_name), 'rb').read()).hexdigest()
        conn.sendall(hash_hex.encode('utf-8'))
        
        ack = conn.recv(1024)
        if ack == b'Success':
            return True
        else:
            return False
        

def main():
    if not os.path.exists(ARCHIVE_FOLDER_NAME):
        os.mkdir(ARCHIVE_FOLDER_NAME)
    
    for i in range(1, 26):
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((HOST, PORT))
        print(f'Connected as Client {i}')
        
        file_choice = FILES[i % 2]
        conn.sendall(file_choice.encode('utf-8'))
        
        file_size = int(conn.recv(1024).decode('utf-8'))
        file_name = f'{i}-Prueba-{i % 2}.txt'
        log_file_name = datetime.datetime.now().strftime(LOG_FILE_NAME_FORMAT)
        with open(log_file_name, 'a') as log_file:
            log_file.write(f'Client {i} requested {file_choice} of size {file_size} using {conn.getsockname()} to {conn.getpeername()}\n')
        
        start_time = datetime.datetime.now()
        success = receive_file(conn, file_size, file_name)
        end_time = datetime.datetime.now()
        
        with open(log_file_name, 'a') as log_file:
            if success:
                log_file.write(f'Client {i} successfully received {file_choice} of size {file_size} using {conn.getsockname()} to {conn.getpeername()} in {end_time - start_time}\n')
                conn.sendall(b'Success')
            else:
                log_file.write(f'Client {i} error receiving {file_choice} of size {file_size} using {conn.getsockname()} to {conn.getpeername()} in {end_time - start_time}\n')
                conn.sendall(b'Error')
        
        conn.close()


if __name__ == '__main__':
    main()
