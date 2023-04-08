import random
from socket import *

# Create a UDP socket
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

while True:
  # Generate random number in the range of 0 to 10
  rand = random.randint(0, 10)
  message, address = serverSocket.recvfrom(1024)
  message = message.upper()
  if rand < 4:
    continue
  serverSocket.sendto(message, address)
