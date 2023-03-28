import socket
import hashlib
import datetime

# define the function to handle a client connection
def handle_client(conn, addr, file_name):
    # receive the request from the client
    
    # check the request and send the file
    with open(file_name, 'rb') as f:
        data = f.read()
        # calculate the hash code for the file data
        hash_code = hashlib.md5(data).hexdigest()
        # send the file and hash code to the client
        conn.send(data)
        conn.send(hash_code.encode('utf-8'))
            
        # receive acknowledgment from client
        ack = conn.recv(1024).decode('utf-8')
            
        # log transfer details
        now = datetime.datetime.now()
        log_file_name = now.strftime("%Y-%m-%d-%H-%M-%S-log.txt")
        with open(log_file_name, 'a') as log_file:
            log_file.write(f"File sent: {file_name}, Size: {len(data)} bytes, Client: {addr}, Successful: {ack == 'OK'}, Time: {datetime.datetime.now()}\n")
    # close the connection
    conn.close()

# create a TCP socket and bind it to a port
host = '192.168.64.10'
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

# listen for incoming connections
s.listen(25)

# wait for more than 25 connections before sending files
while True:
    conn_list = []
    while len(conn_list) < 25:
        # accept a new connection
        conn, addr = s.accept()
        # add the connection to the list
        conn_list.append((conn, addr))
        
    # send the files to all the clients in the list
    for conn, addr in conn_list:
        file_num = int(conn.recv(1024).decode('utf-8'))
        
        if file_num == 1:
            file_name = '10MB.txt'
        elif file_num == 0:
            file_name = '100MB.txt'
        else:
            conn.send('Invalid selection'.encode('utf-8'))
            conn.close()
            continue
        
        # handle the client connection and send the file
        handle_client(conn, addr, file_name)
