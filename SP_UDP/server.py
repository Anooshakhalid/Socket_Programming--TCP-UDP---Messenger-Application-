#CS22104

import socket
import threading
import queue

print("\\***  UDP BASED MESSENGER FOR N CLIENTS ***\\")

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("localhost",9999))  # server receives the msg on this port no
print("UDP server started..")


# handles the message received by a client
#addr = ip +port no
def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)  #max bit of msg
            messages.put((message,addr))

        except:
            pass

# when msg goes into a queue, we immediately broadcast to all the clients
def broadcast():
    while True:
        while not messages.empty(): #messages is a queue, as long as msg in the queue
            message, addr = messages.get()
            print(message.decode()) # server prints and also sends to all
            if addr not in clients:
                clients.append(addr)

            for client in clients: #clients is a list where all client resides
                try:
                    if message.decode().startswith("SIGNUP BY:"): # checks if user joined or not
                        name = message.decode()[message.decode().index(":")+1:]
                        server.sendto(f"{name} has joined the chat!".encode(),client) #all the clients

                    else:
                        server.sendto(message,client)

                except:
                    clients.remove(client)



t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

# loop will run until manually stop


