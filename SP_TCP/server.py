# CS22014

print("\\***  TCP BASED MESSENGER FOR N CLIENTS ***\\")

import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 5555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("TCP server started, waiting for connections...")


clients = []   # Lists For Clients and their names
client_names = []


def broadcast(message): # Sending Messages To All Connected Clients
    for client in clients:
        client.send(message)



def handle(client):# Handling Messages From Clients
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)  # Removing And Closing Clients
            clients.remove(client)
            client.close()
            client_name = client_names[index]
            print(f"{client_name} has disconnected.")
            broadcast('{} has left the chat!'.format(client_name).encode('ascii'))
            client_names.remove(client_name)
            break



def receive():# Receiving / Listening Function
    while True:

        client, address = server.accept()   # Accept Connection
        print("Connected with {}".format(str(address)))

        client.send('NAME'.encode('ascii'))   # Request And Store name
        client_name = client.recv(1024).decode('ascii')
        client_names.append(client_name)
        clients.append(client)

        print("Name is {}".format(client_name))      # Print And Broadcast name
        broadcast("{} has joined the chat!".format(client_name).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,)) # Start Handling Thread For Client
        thread.start()

receive()

