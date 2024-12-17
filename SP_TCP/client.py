import socket
import threading

# Choosing name
client_name = input("Enter your name: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))


# Listening to Server and ending names
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode('ascii')
            if message == 'NAME': # print name of a client
                client.send(client_name.encode('ascii'))
            else:
                print(message)
        except:
            # Close Connection When Error
            print("An error occurred!")
            client.close()
            break



def write():  # Sending Messages To Server
    while True:
        message = '{}: {}'.format(client_name, input(''))
        client.send(message.encode('ascii'))
        # we are not printing it but server continuously receiving the msg


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

