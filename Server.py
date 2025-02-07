from socket import *
import threading
import datetime

SERVER_PORT = 63464
MAX_CLIENTS = 3
clients = []

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(("", SERVER_PORT))
server_socket.listen(MAX_CLIENTS)

print("Server is now listening for connections...")

client_count = 1
client_lock = threading.Lock()


def handle_client(connection_socket, address, client_name):
    global clients

    TimeConnected = datetime.datetime.now()

    with client_lock:
        clients.append({"name": client_name, "started": TimeConnected, "ended": None})

    print(f"Hello {client_name}")

    try:
        while True:
            user_input = connection_socket.recv(1024).decode()
            print(f"Received from {client_name}: {user_input}")

            if user_input == "exit":
                TimeDisconnected = datetime.datetime.now()

                with client_lock:
                    for client in clients:
                        if client['name'] == client_name:
                            client['ended'] = TimeDisconnected
                            print(f"{client_name} disconnected at {TimeDisconnected}")
                            clients.remove(client) 
                            break
                break

            elif user_input == "status":
                status = ""
                for client in clients:
                    TimeDisconnected = client['ended']
                    if TimeDisconnected:
                        status += f"{client['name']}: Connected at {client['started']}, Disconnected at {TimeDisconnected}"
                    else:
                        status += f"{client['name']}: Connected at {client['started']}, Still Connected.."
                
                print(status)
                connection_socket.send(status.encode())

            else:
                connection_socket.send(f"{user_input} ACK".encode())

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        connection_socket.close()
        with client_lock:
            for client in clients:
                if client['name'] == client_name:
                    client['ended'] = datetime.datetime.now()
                    break

wait_for_disconnect = False
while True:
    if len(clients) < MAX_CLIENTS:
        connection_socket, address = server_socket.accept()
        with client_lock:
            client_name = f"Client{client_count:02d}"
            client_count += 1
        threading.Thread(target=handle_client, args=(connection_socket, address, client_name), daemon=True).start()
        wait_for_disconnect = False
    else:
        if not wait_for_disconnect:
            print("Maximum client limit reached. Waiting for a client to disconnect...")
            wait_for_disconnect = True
