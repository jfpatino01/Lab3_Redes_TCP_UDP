import socket
import threading
import time
import os

# Definimos la dirección del servidor y el puerto
SERVER_ADDR = 'localhost'
SERVER_PORT = 12345

# Definimos el tamaño del búfer y el nombre del archivo a descargar
BUFFER_SIZE = 65536 

# Ingresar el numero de clientes
numClientes = int(input("Ingrese el numero de clientes: "))

# Configuración del archivo y el directorio de logs
LOG_DIR = 'Logs'
LOG_FILENAME = time.strftime('(cliente) %Y-%m-%d-%H-%M-%S-log.txt')
LOG_PATH = os.path.join(LOG_DIR, LOG_FILENAME)

# Crear directorio de logs si no existe
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Crear directorio de ArchivosRecibidos si no existe
if not os.path.exists('ArchivosRecibidos'):
    os.mkdir('ArchivosRecibidos')

# Función para recibir el archivo
def receive_file(cliente):
    idCliente = str(cliente)
    try:
        # Creamos un socket UDP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Enviamos el nombre del archivo que deseamos descargar
        client_socket.sendto(idCliente.encode(), (SERVER_ADDR, SERVER_PORT))
        # Creamos un archivo en modo escritura binario

        file_Name, server_address = client_socket.recvfrom(BUFFER_SIZE)

        client_ip, client_port = client_socket.getsockname()


        start_time = time.time()

        with open(os.path.join('ArchivosRecibidos', f'Cliente{cliente}-Prueba-{numClientes}.txt'), 'wb') as f:
            while True:
                # Recibimos los datos del servidor
                data, server_address = client_socket.recvfrom(BUFFER_SIZE)
                # Si recibimos un mensaje vacío, salimos del bucle
                if not data:
                    break
                # Escribimos los datos en el archivo
                f.write(data)
    except Exception as e:
        print(f'Error: {e}')
    finally:
        end_time = time.time()
        transfer_time = end_time - start_time

        # Verificar si la entrega fue exitosa
        if os.path.isfile(os.path.join('ArchivosRecibidos', f'Cliente{cliente}-Prueba-{numClientes}.txt')):
            success = True
        else:
            success = False

        file_size = os.path.getsize((os.path.join('ArchivosRecibidos', f'Cliente{cliente}-Prueba-{numClientes}.txt')))

        # Escribir registro de conexión en el archivo de log
        with open(LOG_PATH, 'a') as log_file:
            log_file.write(f'Cliente: {cliente}, Archivo: {file_Name.decode()}, Tamaño: {file_size} bytes, Exitoso: {success}, Tiempo de transferencia: {transfer_time}, puerto: {client_port}\n')
        # Cerramos el socket
        client_socket.close()

# Creamos varios hilos para descargar el archivo
x = 0
for i in range(numClientes):
    x = x + 1
    threading.Thread(target=receive_file, args=(x,)).start()
