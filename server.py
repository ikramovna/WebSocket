import socket
import threading
import psycopg2

def initialize_database():
    conn = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="1",
        database="chat"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR PRIMARY KEY, in_chat BOOLEAN);")

    conn.commit()
    conn.close()

connected_users = []

def handle_private_chat(user1, user2):
    while True:
        try:
            data = user1['socket'].recv(1024)
            if not data:
                break
            user2['socket'].send(f"{user1['username']}: {data.decode('utf-8')} ".encode('utf-8'))

            data = user2['socket'].recv(1024)
            if not data:
                break
            user1['socket'].send(f"{user2['username']}: {data.decode('utf-8')} ".encode('utf-8'))
        except ConnectionResetError:
            break

    user1['socket'].send("Private chat ended.".encode('utf-8'))
    user2['socket'].send("Private chat ended.".encode('utf-8'))

    user1['socket'].close()
    user2['socket'].close()

    connected_users.remove(user1)
    connected_users.remove(user2)

def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")

    # Get the username from the client
    client_socket.send("Enter your username: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8').strip()

    # Add the user to the database
    cursor = db_conn.cursor()
    cursor.execute("INSERT INTO users (username, in_chat) VALUES (%s, %s) ON CONFLICT (username) DO NOTHING;", (username, False))
    db_conn.commit()

    connected_users.append({'socket': client_socket, 'username': username})

    print(f"{username} connected.")

    # Pair users if possible
    if len(connected_users) >= 2:
        user1 = connected_users.pop(0)
        user2 = connected_users.pop(0)

        print(f"Pairing {user1['username']} with {user2['username']}.")

        # Notify users about the private chat
        user1['socket'].send(f"You are now in a private chat with {user2['username']}".encode('utf-8'))
        user2['socket'].send(f"You are now in a private chat with {user1['username']}".encode('utf-8'))

        private_chat_thread = threading.Thread(target=handle_private_chat, args=(user1, user2))
        private_chat_thread.start()

    else:
        client_socket.send("Waiting for a partner. Please be patient.".encode('utf-8'))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen(5)

print("Server listening on port 5555")

initialize_database()

db_conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="1",
    database="chat"
)

while True:
    client_socket, client_address = server.accept()

    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_handler.start()



