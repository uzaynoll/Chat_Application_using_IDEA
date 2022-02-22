import PySimpleGUI as sg


input_section = [
    [
        sg.In(size=(25,1), enable_events=True, key="input_message"), 
        sg.Button("Send", key="Send")
    ]
]

message = "Welcome to the server!"

username = sg.PopupGetText("Enter username:", no_titlebar=True)
if username == "" or username is None:
    exit()

message += f'{username} joined the chat!'

layout = [
    [sg.Text("Messages", key="user_names")],
    [sg.Column(scrollable=True, vertical_scroll_only=True, size=(500,500), layout=[[sg.Text(message, key="message_box")]], key="Message_box")],
    [
        sg.Column(input_section)
    ]
]

win = sg.Window("Chat Application Using IDEA", layout)

while True:
    event, values = win.read()
    win['message_box'].update(message)
    if event == 'EXIT' or event == sg.WIN_CLOSED:
        break
    if event == 'Send':
        message += "\n" + values['input_message']
        win['message_box'].update(message)
        win['input_message'].update("")

win.close()