import socket
import threading
from Key_generation import create_key
import pickle

HEADERSIZE = 10
HOST = '192.168.100.11'
PORT = 7890

clients = list()
usernames = list()

def receive_client():
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connected: {address}")

        username = client_socket.recv(1024).decode("ascii")
        clients.append(client_socket)
        usernames.append(username)
        msg = pickle.dumps(keys)
        client_socket.send(bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg)

        msg = pickle.dumps({'type':"status",'message':f"{username} joined the chat!"})
        broadcast(bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg)

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

def handle_client(client):
    while True:
        try:
            message = receive_message(client)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            user = usernames[index]
            usernames.remove(user)

            msg = pickle.dumps({'type':"status",'message':f"{user} left the chat!"})
            broadcast(bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg)
            break

def broadcast(message):
    # print(clients)
    for client in clients:
        client.send(message)

def receive_message(client):
    full_message = b''
    new_msg = True
    while True:
        msg = client.recv(512)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_message += msg

        if len(full_message)-HEADERSIZE == msglen:
            new_msg = True
            break
    # print(full_message)
    return full_message

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
keys = create_key()
# print(keys)
print(f"Server initiatied - {HOST}:{PORT}")

server_socket.listen(5)
print ("Socket is listening") 

receive_client()