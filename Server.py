#Imports
from socket import *
import threading
import datetime

#Server port and max clients
SERVER_PORT = 63464
MAX_CLIENTS = 3
#Store clients cache
clients = {}

#Creates the server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", SERVER_PORT))
#Listens up to 3 connections 
serverSocket.listen(MAX_CLIENTS)

print("Server is now listening for connections...")

clientCount = 1

#Lock to access the clients cache
clientLock = threading.Lock()

#list of files
file_repository = ['file1.txt', 'file2.txt', 'file3.txt']

#Main function for communicating with clients
def main(connectionSocket, address, clientName):
    global clients
    #Format date
    Time = datetime.datetime.now()
    TimeConnected = Time.strftime("%x %X")

    #Use lock to modify clients cache
    with clientLock:
        clients[clientName] = {'Connected': TimeConnected, 'Disconnected': "Still Connected.."}

    print(f"Hello {clientName}")

    try:
        #Main loop for communicating to client
        while True:
            #Captures clients input
            user_input = connectionSocket.recv(1024).decode()
            if not user_input:
                break

            print(f"Received from {clientName}: {user_input}")

            #Break loop if user inputs exit
            if user_input.lower() == "exit":
                break  

            #Sends clients cache to client off keyword status 
            elif user_input.lower() == "status":
                with clientLock:
                    status = f"{clientName}: {clients[clientName]}"
                connectionSocket.send(status.encode())

            #Sends file_repository to client off keyword list
            elif user_input.lower() == "list":
                file_list = "\n".join(file_repository)
                connectionSocket.send(file_list.encode())

            #Sends file contents to client off keyword file name
            elif user_input in file_repository:
                try:
                    with open(user_input, 'rb') as file:
                        file_data = file.read()
                    connectionSocket.send(file_data)
                except FileNotFoundError:
                    connectionSocket.send(b"File not found.")

            else:
                #Sends client message back with appended ACK
                connectionSocket.send(f"{user_input} ACK".encode())

    #Catches errors
    except Exception as e:
        print(f"Error with {clientName}: {e}")

    #Once loop is done, prints disconnected time
    finally:
        #Time formatting
        Time = datetime.datetime.now()
        TimeDisconnected = Time.strftime("%x %X")

        with clientLock:
            if clientName in clients:
                clients[clientName]['Disconnected'] = TimeDisconnected
                print(f"{clientName} disconnected at {TimeDisconnected}")
                del clients[clientName]
        connectionSocket.close()

#main server loop to accept clients
while True:
    #Accept new clients if conditions remain true
    connectionSocket, address = serverSocket.accept()
    with clientLock:
        if len(clients) < MAX_CLIENTS:
            clientName = f"Client{clientCount:02d}"
            clientCount += 1
            threading.Thread(target=main, args=(connectionSocket, address, clientName), daemon=True).start()
        else:
            print(f"Server is full.")
            connectionSocket.send(b"Server full. Try again later.")
            connectionSocket.close()
