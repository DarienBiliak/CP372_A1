#Code Before Change
"""
import socket

PORT = 12345

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', PORT))
    client_name = client_socket.recv(1024).decode()
    print(f"Connected to server as {client_name}.")

    while True:
        message = input(f"[{client_name}] Enter message: ")
        client_socket.send(message.encode())

        if message == "exit":
            break
        response = client_socket.recv(1024).decode()
        print(f"[Server] {response}")

        
    client_socket.close()
    print("Disconnected from server.")

if __name__ == '__main__':
    start_client() 
"""
#Code After Change
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
