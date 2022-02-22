from os import system
import socket
import threading

def write(message):
    message = message.encode('utf-8')
    sock.send(message)

def stop():
    sock.close()

def receive():
    while True:
        full_msg = ''
        new_msg = True
        while True:
            msg = sock.recv(16)
            if new_msg:
                # print("new msg len:",msg[:HEADERSIZE])
                msglen = int(msg[:HEADERSIZE])
                new_msg = False

            # print(f"full message length: {msglen}")

            full_msg += msg.decode("utf-8")

            if len(full_msg)-HEADERSIZE == msglen:
                print("full msg recvd")
                print(full_msg[HEADERSIZE:])
                new_msg = True

HOST_IP = 'SHADOW'
PORT = 7890
HEADERSIZE = 10

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((HOST_IP, PORT))
except:
    print("Server not Found")
    input("Enter to exit ...")
    exit()

receive_thread = threading.Thread(target=receive)
receive_thread.start()