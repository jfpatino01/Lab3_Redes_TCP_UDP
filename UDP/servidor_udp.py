import socket
import os
import time


# Definimos la dirección del servidor y el puerto
SERVER_ADDR = 'localhost'
SERVER_PORT = 12345

# Definimos el tamaño del búfer
BUFFER_SIZE = 16384 

# Creamos un socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Asociamos el socket a la dirección y puerto del servidor
server_socket.bind((SERVER_ADDR, SERVER_PORT))

file_name = input("Ingrese el nombre del archivo que quiere enviar: ")
file_size = os.path.getsize(file_name)

# Configuración del archivo y el directorio de logs
LOG_DIR = 'Logs'
LOG_FILENAME = time.strftime('(servidor) %Y-%m-%d-%H-%M-%S-log.txt')
LOG_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

def createLog(cliente, tt):
    # Escribir registro de conexión en el archivo de log
    with open(LOG_PATH, 'a') as log_file:
        log_file.write(f'Cliente: {cliente.decode()}, Archivo: {file_name}, Tamaño: {file_size} bytes, Tiempo de transferencia: {tt}\n')

while True:
    # Recibimos el nombre del archivo que el cliente desea descargar
    ready, client_address = server_socket.recvfrom(BUFFER_SIZE)
    # Abrimos el archivo en modo lectura binario

    server_socket.sendto(file_name.encode(), client_address)

    start_time = time.time()

    with open(file_name, 'rb') as f:
        while True:
            # Leemos los datos del archivo
            data = f.read(BUFFER_SIZE)
            # Si no hay más datos, enviamos un mensaje vacío para indicar el fin del archivo
            if not data:
                server_socket.sendto(b'', client_address)
                end_time = time.time()
                transfer_time = end_time - start_time
                createLog(ready, transfer_time)
                break
            # Enviamos los datos al cliente
            server_socket.sendto(data, client_address)
    

