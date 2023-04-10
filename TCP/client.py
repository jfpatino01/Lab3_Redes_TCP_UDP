import socket
import hashlib
import os
import datetime
import threading

HOST = '127.0.0.1'
PORT = 5555
FILES = [
    '250MB.txt',
    '100MB.txt',
]
LOG_FILE_NAME_FORMAT = '%Y-%m-%d-%H-%M-Client-log.txt'
ARCHIVE_FOLDER_NAME = 'ArchivosRecibidos'
BUFFER_SIZE = 1024 * 1024 * 250

def receive_file(conn, file_size, file_name):
    data_received = 0
    with open(os.path.join(ARCHIVE_FOLDER_NAME, file_name), 'wb') as f:
        while data_received < file_size:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
            data_received += len(data)
        f.flush()
        hash_hex = hashlib.sha256(open(os.path.join(ARCHIVE_FOLDER_NAME, file_name), 'rb').read()).hexdigest()
        conn.sendall(hash_hex.encode('utf-8'))
        
        ack = conn.recv(BUFFER_SIZE)
        if ack == b'Success':
            return True
        else:
            return False
        

def clientrun(i, j):
    print(f"Running clientrun({i}, {j})")

    fileToSend=int(j)
    
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((HOST, PORT))

    file_choice = FILES[fileToSend]
    conn.sendall(file_choice.encode('utf-8'))
    
    file_size = int(conn.recv(BUFFER_SIZE).decode('utf-8'))
    file_name = f'{i}-Prueba-{fileToSend}.txt'
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


if not os.path.exists(ARCHIVE_FOLDER_NAME):
    os.mkdir(ARCHIVE_FOLDER_NAME)
j = input("Enter a value for j: ")
threads = []
for i in range(1, 26):
    t = threading.Thread(target=clientrun, args=(i, j))
    t.start()
    threads.append(t)

# Wait for all threads to complete
for t in threads:
    t.join()