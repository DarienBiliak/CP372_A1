#Imports
from socket import *

serverName = "localhost"
serverPort = 63464

try:

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    while True:
        user = input("Input a lowercase sentence: ")
        clientSocket.send(user.encode())

        if user.lower() == "exit":
            break

        data = clientSocket.recv(1024).decode()
        print("From Server:", data)
        
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    clientSocket.close()
    print("Connection closed.")