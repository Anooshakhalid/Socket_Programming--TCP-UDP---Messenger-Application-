import random
import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost",random.randint(8000, 9000)))

name = input("Your Name:")

def recieve():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

# continuously listens, send and receive msgs
t = threading.Thread(target=recieve)
t.start()
client.sendto(f"SIGNUP BY: {name}".encode(),("localhost",9999))

while True:
    message = input("")
    if message == "exit":
        exit()
    else:
        client.sendto(f"{name}:{message}".encode(),("localhost",9999))


