from socket import *
import threading
import datetime

SERVER_PORT = 63464
MAX_CLIENTS = 3
clients = {}

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", SERVER_PORT))
serverSocket.listen(MAX_CLIENTS)

print("Server is now listening for connections...")

clientCount = 1
clientLock = threading.Lock()

file_repository = ['file1.txt', 'file2.txt', 'file3.txt']

def main(connectionSocket, address, clientName):
    global clients

    #Date formatting
    Time= datetime.datetime.now()
    TimeConnected = Time.strftime("%x %X")

    with clientLock:
        clients[clientName] = {'Connected': TimeConnected, 'Disconnected': "Still Connected.."}

    print(f"Hello {clientName}")

    try:
        while True:
            user_input = connectionSocket.recv(1024).decode()
            print(f"Received from {clientName}: {user_input}")

            if user_input == "exit":
                #Date formatting
                Time = datetime.datetime.now()
                TimeDisconnected = Time.strftime("%x %X")

                with clientLock:
                    clients[clientName]['Disconnected'] = TimeDisconnected
                    print(f"{clientName} disconnected: {TimeDisconnected}")
                    del clients[clientName]
                     
                break

            elif user_input == "status":
                with clientLock:
                    status = f"{clientName}: {clients[clientName]}"
                print(status)
                connectionSocket.send(status.encode())

            elif user_input == "list":
                file_list = "\n".join(file_repository)
                connectionSocket.send(file_list.encode())

            elif user_input in file_repository:
                file_name = user_input
                try:
                    with open(file_name, 'rb') as file:
                        file_data = file.read()
                    connectionSocket.send(file_data)
                except FileNotFoundError:
                    connectionSocket.send(b"File not found.")

            else:
                connectionSocket.send(f"{user_input} ACK".encode())

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        connectionSocket.close()
        

waitDisconnect = False
while True:
    if len(clients) <= MAX_CLIENTS:
        connectionSocket, address = serverSocket.accept()
        with clientLock:
            clientName = f"Client{clientCount:02d}"
            clientCount += 1
        threading.Thread(target=main, args=(connectionSocket, address, clientName), daemon=True).start()
        waitDisconnect = False
    else:
        if not waitDisconnect:
            print("Maximum client limit reached. Waiting for a client to disconnect...")
            waitDisconnect = True
            connectionSocket.close()
