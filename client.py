import socket
import threading


def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except ConnectionResetError:
            # Handle disconnection
            print("Disconnected from the server.")
            break


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

welcome_message = client.recv(1024).decode('utf-8')
print(welcome_message)

receive_thread = threading.Thread(target=receive_messages, args=(client,))
receive_thread.start()

while True:
    try:
        message = input()
        client.send(message.encode('utf-8'))
    except (EOFError, KeyboardInterrupt):
        print("You have left the chat.")
        break
