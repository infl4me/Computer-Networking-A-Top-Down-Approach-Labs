from socket import *
import json

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()

    server_integer = 42

    client_data = json.loads(connectionSocket.recv(1024).decode('utf-8'))
    client_message = client_data['message']
    client_integer = client_data['integer']

    if client_integer < 1 or client_integer > 100:
        connectionSocket.close()
        break

    print(f'Message received: "{client_message}"')
    print("Sum: ", server_integer + client_integer)

    reply_data = { 'message': 'Server of John Q. Smith', 'integer': server_integer  }
    connectionSocket.send(json.dumps(reply_data).encode('utf-8'))
    
    connectionSocket.close()
