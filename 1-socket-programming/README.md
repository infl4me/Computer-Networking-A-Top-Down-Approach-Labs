## Socket Programming Lab

In this assignment, you’ll write a client that will use sockets to communicate with a server that you will also write. 

Here’s what your client and server should do:

1. The client should first accept an integer between 1 and 100 from the keyboard, open a TCP socket to your server and send a message containing (i) a string containing your name (e.g., “Client of John Q. Smith”) and (ii) the entered integer value and then wait for a sever reply.

2. The server will create a string containing its name (e.g., “Server of John Q. Smith”) and then begin accepting connections from clients. On receipt of a client message, your server should:
   - print (display) the client’s name (extracted from the received message) and the server’s name
   - itself pick an integer between 1 and 100 (it’s fine for the server to use the same number all the time) and display the client’s number, its number, and the sum of those numbers
   - send its name string and the server-chosen integer value back to the client
   - if your server receives an integer value that is out of range, it should terminate after releasing any created sockets. You can use this to shut down your server.

3. The client should read the message sent by the server and display its name, the server’s name, its integer value, and the server’s integer value, and then compute and the sum. The client then terminates after releasing any created sockets. 

As an aside (and as a check that you are doing things correctly, you should make sure for yourself that the values and the sums are correct!)
