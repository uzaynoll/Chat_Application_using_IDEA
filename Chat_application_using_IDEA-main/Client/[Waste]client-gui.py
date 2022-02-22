import tkinter
import tkinter.simpledialog, tkinter.ttk
from tkinter.constants import BOTH, BOTTOM, LEFT, TOP, VERTICAL

root = tkinter.Tk()
root.title("Chat Application Using IDEA")
root.geometry("500x500")
# root.minsize(500, 500)
# root.maxsize(500, 500)

username = tkinter.simpledialog.askstring(title="Test", prompt="Enter username:")
lab = tkinter.Label(root, text=username)
lab.pack()  

def send_message():
    msg = input_message.get()
    input_message.delete(0, tkinter.END)
    tkinter.Label(second_frame, text=msg).pack(pady=5, padx=10, side= TOP, anchor="w")

title = tkinter.Label(root, text="Chat Application")
frame = tkinter.Frame(root)
messages = tkinter.Canvas(frame)
scrollbar = tkinter.ttk.Scrollbar(frame, orient=VERTICAL, command=messages.yview)
input_frame = tkinter.Frame(root)
input_message = tkinter.Entry(input_frame, width=65)
send_button = tkinter.Button(input_frame, text="Send", pady=5, padx=10, command=send_message)

title.pack(side= TOP, anchor="n")
frame.pack( fill=BOTH)
scrollbar.pack(side="right",fill="y")
messages.config(yscrollcommand = scrollbar.set)
messages.bind('<Configure>', lambda e: messages.configure(scrollregion=messages.bbox("all")))

second_frame = tkinter.Frame(messages)

messages.create_window((0,0), window=second_frame, anchor='w')

messages.pack(side= TOP, anchor="w", fill=BOTH)
input_frame.pack(pady=20, side= BOTTOM, anchor="w")
input_message.pack(side= LEFT, anchor="center",padx=10)
send_button.pack(side= LEFT, anchor="n",padx=10)

root.mainloop()