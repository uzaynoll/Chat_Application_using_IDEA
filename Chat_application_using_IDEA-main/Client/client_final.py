import socket
import threading
import pickle
from encryption import encrypt
from decryption import decrypt
import PySimpleGUI as sg
from time import sleep

HEADERSIZE = 10
HOST = socket.gethostbyname(socket.gethostname())
PORT = 7890

USERNAME = sg.PopupGetText("Enter username:", no_titlebar=True)
if USERNAME == "" or USERNAME is None:
    exit()

message_history = ""
launch = True

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
    global message_history, launch
    while True:
        try:
            full_message = b''
            new_msg = True
            print("*"*100+f"\nRecieving message\n")
            while True:
                msg = client_socket.recv(512)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_message += msg

                if len(full_message)-HEADERSIZE == msglen:
                    new_msg = True
                    break
            print("*"*100+"\nMessage received successfully\n")
            message = pickle.loads(full_message[HEADERSIZE:])

            if message['type'] == 'status':

                print("\t"+"-"*80+f"\n\tDECRYPTION NOT REQUIRED\n")

                message_history += message['message'] + "\n"+"-"*113+"\n"  
            elif message['type'] == 'data':
                message_history += decrypt(message['message'], keys['decrypt']) + "\n"+"-"*113+"\n" 
            
            if not launch:
                win['message_box'].update(message_history) 
        except:
            message_history += "--Error Occurred--"
            client_socket.close()
            break
    
def send_message(input_message):
    message = f'{USERNAME}: ' + input_message

    print("*"*100+f"\nSending message\n")
    print("\t"+"-"*80+f"\n\t'{USERNAME}:' attached to message \n")
    print("\t"+"-"*80+f"\n\tEncrypting the message: {message} \n")

    encrypt_msg = encrypt(message, keys['encrypt'])
    msg = pickle.dumps({'type':"data",'message':encrypt_msg})
    client_socket.send(bytes(f"{len(msg):<{HEADERSIZE}}", 'utf-8') + msg)
    print("\nMessage sent successfully\n")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(USERNAME.encode("ascii"))
keys = receive_keys()
print("Successfully recieved keys!!")

def create_gui(messages):
    input_section = [
        [
            sg.In(size=(60,1), enable_events=True, key="input_message", focus=True), 
            sg.OK("Send", key="Send")
        ]
    ]

    layout = [
        [sg.Text("Messages", background_color='white', text_color='black')],
        [sg.Column( layout=[[sg.Multiline(messages, key="message_box", size=(65,25) , autoscroll=True, disabled=True, background_color='white', text_color='black')]], background_color='white')],
        [
            sg.Column(input_section, background_color='white')
        ]
    ]

    return sg.Window("Chat Application Using IDEA", layout, background_color='white')

if launch:
    receive_thread = threading.Thread(target=receive_message)
    receive_thread.start()
    sleep(1)
    launch = False
    win = create_gui(message_history)

while True:
    event, values = win.read()

    if event == 'EXIT' or event == sg.WIN_CLOSED:
        client_socket.close()
        break

    if event == 'Send' and values['input_message'] != '' :
        send_message(values['input_message'])
        win['input_message'].update("")

win.close()
