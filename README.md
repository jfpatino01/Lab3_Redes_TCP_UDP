# Lab3_Redes_TCP_UDP
Desarollado para probar TCP y UDP durante 2023-10 para la clase de Infraestructura de Comunicaciones
Sección 2 Grupo 3

## Instrucciones para ejecutar TCP

1. Clonar repositorio en dos maquinas diferentes para ser sevidor y cliente. Si se usa MV se debe usar Bridge.
2. Ejecutar el creador de archivos para generar archivo de 250MB en el servidor
3. Editar el archivo server.py para insertar el IP del a Maquina Host del Servidor y Puerto deseado
4. Ejecutar Servidor
5. Editar, en la maquina del cliente, el archivo client.py para apuntar al IP y Puerto del servidor
6. Ejecutar Cliente y solicitar un archivo (0 o 1)

## Instrucciones para ejecutar UDP

1. Generar desde este [Link](https://generatefile.com/) dos archivos uno de 100MB y otro de 250MB, nombrarlos 100MB.txt y 250MB.txt respectivamente y guardarlos en la carpeta UDP. Ejecutar desde la terminal python servidor_udp.py e ingresar el uno de los nombres de los archivos guardados anteriormente. Luego en otra terminal ejecutar python cliente_udp.py e ingresar el nummero de clientes a utilizar. Una vez hecho esto el programa empezara a correr y vera en las carpetas ArchivosRecibidos y Logs los resultados.


