# import socket module
from socket import *
import sys  # In order to terminate the program
import os 

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))
serverSocket.listen(1)

dir_path = os.path.dirname(os.path.realpath(__file__))

print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode('utf-8')
        filename = message.split()[1]
        f = open(dir_path + '/' +filename[1:])
        outputdata = f.read()

        response_lines = [
            'HTTP/1.1 200 OK',
            'Content-Type: text/html; charset=UTF-8',
            'Content-Length: ' + str(len(outputdata)),
            '',
            outputdata,
            ''
        ]
        response = '\r\n'.join(response_lines)

        connectionSocket.send(response.encode('utf-8'))

        connectionSocket.close()
    except IOError:
        outputdata = 'Not found'
        response_lines = [
            'HTTP/1.1 404 Not Found',
            'Content-Type: text/html; charset=UTF-8',
            'Content-Length: ' + str(len(outputdata)),
            '',
            outputdata,
            ''
        ]
        response = '\r\n'.join(response_lines)

        connectionSocket.send(response.encode('utf-8'))
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
