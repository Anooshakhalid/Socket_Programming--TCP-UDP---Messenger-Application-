import socket
import threading
import tkinter as tk
from tkinter import scrolledtext



# Choosing name
client_name = input("Enter your name: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))



# Function to create the GUI
def create_gui(client, client_name):
    # Create the main window
    root = tk.Tk()
    root.title("Chat Client")

    # Set background color for the window
    root.config(bg="#F8F8FF")  # Light background color for the window

    # Create a ScrolledText widget to display chat messages (shared chat bar)
    chat_display = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20, wrap=tk.WORD, bg="#ffe6f2", fg="black", font=("Arial", 12))
    chat_display.grid(row=0, column=0, padx=10, pady=10)

    # Create an Entry widget to type messages
    message_entry = tk.Entry(root, width=50, font=("Arial", 12))
    message_entry.grid(row=1, column=0, padx=10, pady=10)

    # Function to send a message
    def send_message():
        message = message_entry.get()
        if message:
            message_entry.delete(0, tk.END)
            formatted_message = '{}: {}'.format(client_name, message)
            client.send(formatted_message.encode('ascii'))
            display_message(formatted_message)  # Display the message you send




    # Function to display messages in the chat display
    def display_message(message):
        chat_display.config(state='normal')  # Enable editing of the text widget
        chat_display.insert(tk.END, message + '\n')  # Add message to the display
        chat_display.yview(tk.END)  # Scroll to the bottom of the chat display
        chat_display.config(state='disabled')  # Disable editing of the text widget

    # Create a Send button
    send_button = tk.Button(root, text="Send", width=20, command=send_message, font=("Arial", 12), bg="#ff80bf", fg="white")
    send_button.grid(row=1, column=1, padx=10, pady=10)




    # Listening to Server and Sending Nickname
    def receive():
        while True:
            try:
                message = client.recv(1024).decode('ascii')
                if message == 'NAME':
                    client.send(client_name.encode('ascii'))
                else:
                    # Check if the message indicates someone left the chat
                    if "left the chat" in message:
                        message = message + " (this user has disconnected)"
                    # Display received message if it's not your own
                    if not message.startswith(f"{client_name}:"):  # Avoid showing the same message twice
                        root.after(0, display_message, message)  # Safely update the GUI
                    elif message.startswith(f"{client_name}:") and message != '{}: {}'.format(client_name, message.split(": ", 1)[1]):
                        root.after(0, display_message, message)  # Display your own message once
            except:
                print("An error occurred!")
                client.close()
                break

    # Thread to receive messages
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    # Start the Tkinter main loop
    root.mainloop()

# Start the GUI
create_gui(client, client_name)
