from socket import *
import json

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

input_value = input('Input an integer between 1 and 100: ')
client_integer = int(input_value)

data = {'message': 'Client of John Q. Smith', 'integer': client_integer }
clientSocket.send(json.dumps(data).encode('utf-8'))

server_data = json.loads(clientSocket.recv(1024).decode('utf-8'))
server_message = server_data['message']
server_integer = server_data['integer']

print('Message from server: ', server_message)
print("Sum: ", server_integer + client_integer)

clientSocket.close()
