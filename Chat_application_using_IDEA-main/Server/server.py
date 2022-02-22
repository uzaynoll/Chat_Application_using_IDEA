import socket
import threading
import select

HEADERSIZE = 10
PORT = 7890
socket_list = list()
client_list = dict()

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADERSIZE)

        if not len(message_header):
            return False

        message_length = int(message_header.decode('utf-8').strip())

        return {'header': message_header, 'data': client_socket.recv(message_length)}

    except:
        return False

def receive_client():
    while True:
        c, addr = server_socket.accept()    
        print ('Got connection from', addr )

        msg = "Welcome to the server!"
        msg = f"{len(msg):<{HEADERSIZE}}" + msg

        c.send(bytes(msg,"utf-8"))


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# This modifies the socket to allow us to reuse the address.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host_ip = socket.gethostname()
server_socket.bind((host_ip, PORT))
print(f"Server initiatied - {host_ip}:{PORT}")

server_socket.listen(5)
print ("Socket is listening") 

socket_list.append(server_socket)

receive_client_thread = threading.Thread(target=receive_client)
receive_client_thread.start()