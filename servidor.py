import socket
import threading

host = '127.0.0.1'  # LOCALHOST
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Servidor ejecutándose en {host}:{port}")

clients = []
user_names = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                clients.remove(client)
                client.close()

def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        except Exception as e:
            print(f"Error en handle_messages: {e}")
            break
    # Clean up after disconnection
    index = clients.index(client)
    user_name = user_names[index]
    broadcast(f"Chatbot: {user_name} se desconectó".encode("utf-8"), client)
    clients.remove(client)
    user_names.remove(user_name)
    client.close()

def receive_connections():
    while True:
        try:
            client, address = server.accept()
            client.send("@username".encode("utf-8"))
            user_name = client.recv(1024).decode("utf-8")

            clients.append(client)
            user_names.append(user_name)

            print(f"{user_name} está conectado desde {address}")

            message = f"ChatBot: {user_name} se unió al chat".encode("utf-8")
            broadcast(message, client)
            client.send("Conectado al servidor".encode("utf-8"))

            thread = threading.Thread(target=handle_messages, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error al aceptar conexiones: {e}")

receive_connections()
