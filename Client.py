#Imports
from socket import *

#Create server name and port number
serverName = "localhost"
serverPort = 63464

#Create TCP socket and connect to server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# Sets a timeout for socket operation to 2 seconds
clientSocket.settimeout(2) 

try:
    #Receive data from the server
    server_response = clientSocket.recv(1024).decode()

    #Server full response
    if server_response == "Server full. Try again later.":
        print(server_response)  
        clientSocket.close()
        exit() 

#Ignore error and continue
except timeout:
    pass  

#Infinite loop to interact with user and server
while True:
    userInput = input("Input a lowercase sentence: ")
    clientSocket.send(userInput.encode())

    #Breaks out of loop if user enters exit
    if userInput.lower() == "exit":
        break

    #Receive the server's response
    data = clientSocket.recv(1024).decode()
    print("From Server:", data)

#Closes the socket after loop is done
clientSocket.close()
print("Disconnected from server.")
