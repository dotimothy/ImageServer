# HTTPS Web Server for TheDoLab #
# Socket Implementation #
# Author: Timothy Do 
# Last Revision: 7/16/22

#import socket module
from socket import *
import os
import time

# create an IPv4 TCP socket
#Fill in start 
serverSocket = socket(AF_INET,SOCK_STREAM)     
#Fill in end

# Server Socket Variables %
serverIP  = "0.0.0.0" 
serverPort = 80 
responses = {
    202: b'HTTP/1.1 200 OK\r\n\r\n',
    404: b'HTTP/1.1 404 Not Found\r\n\r\n'
}

# Prepare a sever socket
#Fill in start  
serverSocket.bind((serverIP,serverPort))
#Fill in end

# Listen for connections from client 
#Fill in start     
serverSocket.listen(1)
#Fill in end
print ("Hosting Server on Port " + str(serverPort) + " and Listening...")
while True:
    # Establish the connection
    
    connectionSocket, addr = serverSocket.accept()
    print("Accpeted Connection from " + str(addr[0]) + ":" + str(addr[1]))
    try:
        message = connectionSocket.recv(1024).decode()
        message_split = message.split()
        if len(message_split) <= 1:
            # Small connection from browser - ignore
            connectionSocket.close()
            continue
            
        filename = message_split[1]
        if(filename == "/"):
            filename = "/index.html"
            
        if(filename == "/imageserver.py"):
            outputdata = b'Permission Denied.'
        elif(filename == "/closeimageserver"):
            outputdata = b'Exiting Image Server'
        else:
            f = open(filename[1:], "rb")
            try:
                outputdata = f.read()
            except IOError:
                print("woops!")
                filename.append(".html")
                f = open(filename[1:],"rb")
                outputdata = f.read()
        
        # Send one HTTP header line into socket
        #Fill in start
        connectionSocket.send(responses[202])
        #Fill in end
        
        # Send the content of the requested file to the client
        #Fill in start     
        connectionSocket.send(outputdata)
        #Fill in end
        
        # Close client socket
        #Fill in start
        connectionSocket.close()     
        #Fill in end
        if(filename == "/closeimageserver"):
            print("Exiting Image Server...")
            exit()
       
    except IOError:
        try: #see if filename is html
            filename = filename + ".html"
            f = open(filename[1:],"rb")
            outputdata = f.read()
            connectionSocket.send(responses[202])
            connectionSocket.send(outputdata)
        except IOError:
            # Send response message for file not found
            connectionSocket.send(responses[404])
            nf = open('404.html',"rb")
            fourofour = nf.read() 
            connectionSocket.send(fourofour)
            
            # Close client socket
            #Fill in start  
            connectionSocket.close()   
            #Fill in end
    except KeyboardInterrupt:
        # User pressed Ctrl+C, exit gracefully
        break
        
# Close server connection
serverSocket.close()
