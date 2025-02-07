from socket import *

serverName = "localhost"
serverPort = 63464

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    userInput = input("Input a lowercase sentence: ")
    clientSocket.send(userInput.encode())

    if userInput.lower() == "exit":
        break

    data = clientSocket.recv(1024).decode()
    print("From Server:", data)
    
clientSocket.close()
print("Disconnected from server.")
