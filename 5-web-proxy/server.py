from socket import *
import sys

MAX_RESPONSE_SIZE = 1024 * 1024 * 5

if len(sys.argv) <= 1:
  print(
    'Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
  sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind((sys.argv[1], int(sys.argv[2])))
tcpSerSock.listen(1)

while 1:
  # Strat receiving data from the client
  print('Ready to serve...')
  tcpCliSock, addr = tcpSerSock.accept()
  print('Received a connection from:', addr)
  message = tcpCliSock.recv(1024).decode()
  print('message: ', message)
  # Extract the filename from the given message
  print('message split: ', message.split()[1])
  filename = message.split()[1].partition("/")[2]
  print('filename: ', filename)

  cacheFilePath = "./cache/" + filename
  isCached = False

  try:
    # Check wether the file exist in the cache
    file = open(cacheFilePath, "r")
    isCached = True

    print('Reading from cache...')

    cacheData = file.read(MAX_RESPONSE_SIZE)
    file.close()

    tcpCliSock.send(cacheData.encode())
  except IOError:
    if isCached == False:
      try:
        hostn = filename.replace("www.", "", 1)
        print('hostn', hostn)
        c = socket(AF_INET, SOCK_STREAM)
        c.connect((hostn, 80))

        httpRequest = "GET / HTTP/1.0\r\n\r\n"
        print('request', httpRequest)
        c.send(httpRequest.encode())
        raw_response = c.recv(MAX_RESPONSE_SIZE)

        print('Writing to cache...')
        cacheFile = open(cacheFilePath, "wb")
        cacheFile.write(raw_response)
        cacheFile.close()

        response = raw_response.decode()
        print('RESPONSE: ', response, len(response))

        tcpCliSock.send(raw_response)

        c.close()
      except Exception as inst:
        print("Illegal request", inst)
    else:
      # HTTP response message for file not found
      tcpCliSock.send("HTTP/1.0 404 sendErrorErrorError\r\n".encode())
      tcpCliSock.send("Content-Type:text/html\r\n".encode())
      tcpCliSock.send("\r\n".encode())
  # Close the client and the server sockets
  tcpCliSock.close()
tcpSerSock.close()
