#Billy Burnett
#fed507

from socket import * #import socket module
import sys # In order to terminate the program
import errno
import os

#Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[1])
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
print('The server is ready to receive')
while True:
    try:
        #Establish the connection
        print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        #Decode and open message from socket
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        print(message)
        outputdata = f.read()
        #Send one HTTP header line into socket
        connectionSocket.send("HTTP/1.1 200 OK\n".encode())
        #Send the content of the requested file to the client and close the client socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()
    except IOError:
    #Send response message for file not found/stop request
        if filename.lower() == "/stop":
            connectionSocket.send("Stop Requested".encode())
            break
        else:
            connectionSocket.send("HTTP/1.1 404 Not Found".encode())
        connectionSocket.close()
    #Exit loop if CTRL+C is input
    except KeyboardInterrupt:
        if connectionSocket is not None:
            connectionSocket.close()
        print()
        break
#Close program
print("Have a nice day!")
serverSocket.close()
sys.exit()
