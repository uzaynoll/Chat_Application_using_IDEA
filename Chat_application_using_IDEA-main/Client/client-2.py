import socket
import threading
import pickle
from encryption import encrypt
from decryption import decrypt

HEADERSIZE = 10
HOST = '192.168.100.11'
PORT = 7890
USERNAME = input("Choose a username: ")

def receive_keys():
    full_message = b''
    new_msg = True
    while True:
        msg = client_socket.recv(512)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False

        full_message += msg

        if len(full_message)-HEADERSIZE == msglen:
            new_msg = True
            break
    return pickle.loads(full_message[HEADERSIZE:])

def receive_message():
    while True:
        try:
            full_message = b''
            new_msg = True
            while True:
                msg = client_socket.recv(512)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_message += msg

                if len(full_message)-HEADERSIZE == msglen:
                    new_msg = True
                    break
            message = pickle.loads(full_message[HEADERSIZE:])
            # print(message)
            if message['type'] == 'status':
                print(message['message'])
            elif message['type'] == 'data':
                print(decrypt(message['message'], keys['decrypt']))
        except:
            print("Error Occurred!")
            client_socket.close()
            break

def send_message():
    while True:
        message = f'{USERNAME}: ' + input("")
        encrypt_msg = encrypt(message, keys['encrypt'])
        msg = pickle.dumps({'type':"data",'message':encrypt_msg})
        client_socket.send(bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(USERNAME.encode("ascii"))
keys = receive_keys()
# print("Successfully received keys!!")

receive_thread = threading.Thread(target=receive_message)
receive_thread.start()

send_thread = threading.Thread(target=send_message)
send_thread.start()