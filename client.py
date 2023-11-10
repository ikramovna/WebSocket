import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            # Receive and display messages from the server
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            # Handle disconnection
            print("Disconnected from the server.")
            break

# Client setup
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))  # Connect to the server, no need to bind

# Receive a welcome message
welcome_message = client.recv(1024).decode('utf-8')
print(welcome_message)

# Start a thread to receive messages
receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

# Send messages to the server
while True:
    try:
        message = input()
        client.send(message.encode('utf-8'))
    except (EOFError, KeyboardInterrupt):
        # Handle Ctrl+C or EOF (e.g., when the user closes the terminal)
        print("You have left the chat.")
        break


