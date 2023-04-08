from socket import *
import time

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

for i in range(1, 11):
  message = f'Ping {i + 1} time'

  try:
    start = time.time_ns()

    clientSocket.sendto(message.encode(), (serverName, serverPort))
    clientSocket.settimeout(1.0)
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

    end = time.time_ns()

    time_elapsed = round((end - start) / 1000000.0, 3)

    print(
        f'Ping {i}: RTT: {time_elapsed} ms; Message: {modifiedMessage.decode()}')
  except TimeoutError:
    print(f'Ping {i}: Request timed out')

clientSocket.close()
