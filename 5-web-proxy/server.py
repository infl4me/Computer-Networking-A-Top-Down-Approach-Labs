from socket import *
import sys

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
  fileExist = "false"
  filetouse = "/" + filename
  print('filetouse: ', filetouse)
  try:
    # Check wether the file exist in the cache
    f = open(filetouse[1:], "r")
    outputdata = f.readlines()
    fileExist = "true"
    # ProxyServer finds a cache hit and generates a response message
    tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
    tcpCliSock.send("Content-Type:text/html\r\n".encode())
    for i in range(0, len(outputdata)):
      tcpCliSock.send(outputdata[i].encode())
      print('Read from cache')
  # Error handling for file not found in cache
  except IOError:
    if fileExist == "false":
      # Create a socket on the proxyserver
      # c = socket(AF_INET, SOCK_STREAM)
      hostn = filename.replace("www.", "", 1)
      print('hostn', hostn)
      try:
        c = socket(AF_INET, SOCK_STREAM)
        c.connect((hostn, 80))

        http_request = "GET / HTTP/1.0\r\n\r\n"
        print('request', http_request)
        c.send(http_request.encode())
        response = c.recv(1024 * 1024 * 5).decode()
        print('RESPONSE: ', response, len(response))

        tcpCliSock.send(response.encode())

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
