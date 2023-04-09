import socket
import os
import base64

smtp_username = base64.b64encode(os.environ['SMTP_USERNAME'].encode('ascii')).decode()
smtp_password = base64.b64encode(os.environ['SMTP_PASSWORD'].encode('ascii')).decode()

smtp_server = 'sandbox.smtp.mailtrap.io'
smtp_port = 2525

mail_to_user = 'to@example.com'
mail_from_user = 'from@example.com'

email_body_lines = [
  'To: to@example.com',
  'From: from@example.com',
  'Subject: Hello world!',
  '',
  'This is the test message...',
  '.',
  ''
]
email_body = '\r\n'.join(email_body_lines)

# Create socket called client_socket and establish a TCP connection with mailserver
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((smtp_server, smtp_port))

recv = client_socket.recv(1024).decode()
print(recv)

if recv[:3] != '220':
  print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'

client_socket.send(heloCommand.encode())
recv1 = client_socket.recv(1024).decode()
print(recv1)

if recv1[:3] != '250':
  print('250 reply not received from server.')

# Send AUTH command with credentials
client_socket.send(f'AUTH LOGIN\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

client_socket.send(f'{smtp_username}\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

client_socket.send(f'{smtp_password}\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

# Send MAIL FROM command and print server response.
client_socket.send(f'MAIL FROM:<{mail_from_user}>\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

# Send RCPT TO command and print server response.
client_socket.send(f'RCPT TO:<{mail_to_user}>\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

# Send DATA command and print server response.
client_socket.send(f'DATA\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())

client_socket.send(email_body.encode())
response = client_socket.recv(1024)
print(response.decode())

# Send QUIT command and get server response.
client_socket.send(f'quit\r\n'.encode())
response = client_socket.recv(1024)
print(response.decode())
