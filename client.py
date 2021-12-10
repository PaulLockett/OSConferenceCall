from serverlib import *
import tkinter as tk
import tkinter.scrolledtext as tkst
import tkinter.simpledialog as tkSimpleDialog
import sys
import socket
import threading

 
label_tartget_ip = ""

gui_rendered = False

if label_tartget_ip:
    client = StreamingClient(label_tartget_ip, 9999)
    receiver = AudioClient(label_tartget_ip, 8888)
    chatRoom = ChatClient(label_tartget_ip, 7777)

def start_listening():
    t1 = threading.Thread(target=client.start_listening)
    t2 = threading.Thread(target=receiver.start_listening)
    t3 = threading.Thread(target=start_chat)
    t1.start()
    t2.start()
    t3.start()

def start_camera_stream():
    t3 = threading.Thread(target=client.start_streaming)
    t3.start()

def start_audio_stream():
    t4 = threading.Thread(target=receiver.start_stream)
    t4.start()

def disconnect():
    client.disconnect()
    receiver.disconnect()

    while(not gui_rendered):
        pass

    chatRoom.send(f"{username} has left the room".encode())

    sys.exit()

def send_message(event=None):
    message = input_area.get("1.0", tk.END)
    chatRoom.send((username + ":" + message).encode())
    input_area.delete("1.0", tk.END)

def start_chat():
    # fill the chat_box with messages from the server
    while(not gui_rendered):
        pass

    chatRoom.send(f"{username} has joined the room".encode())

    while True:
        try:
            message = chatRoom.receive()
            if gui_rendered:
                text_area.config(state=tk.NORMAL)
                text_area.insert(tk.END, message.decode() + '\n')
                text_area.yview(tk.END)
                text_area.config(state=tk.DISABLED)
        except:
            break

window = tk.Tk()
window.title("Client")
window.geometry("300x300")

text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()

btn_listen = tk.Button(window, text="connect to server", width=50, command=start_listening)
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_camera = tk.Button(window, text="Start Camera", width=50, command=start_camera_stream)
btn_camera.pack(anchor=tk.CENTER, expand=True)

btn_audio = tk.Button(window, text="Start Audio", width=50, command=start_audio_stream)
btn_audio.pack(anchor=tk.CENTER, expand=True)

btn_disconnect = tk.Button(window, text="Disconnect", width=50, command=disconnect)
btn_disconnect.pack(anchor=tk.CENTER, expand=True)

server_address = tkSimpleDialog.askstring("Server Address", "Enter the server address:")

if server_address:
    client = StreamingClient(server_address, 9999)
    receiver = AudioClient(server_address, 8888)
    chatRoom = ChatClient(server_address, 7777)

username = tkSimpleDialog.askstring("Username", "Please enter your username:")

chatWindow = tk.Toplevel(window)
chatWindow.config(bg="lightgray")
chatWindow.protocol("WM_DELETE_WINDOW", disconnect)

chat_label = tk.Label(chatWindow, text="Chat:", bg="lightgray")
chat_label.config(font=("Courier", 18))
chat_label.pack(padx=20, pady=5)

text_area = tkst.ScrolledText(chatWindow)
text_area.pack(padx=20, pady=5)
text_area.config(state=tk.DISABLED)

msg_label = tk.Label(chatWindow, text="Message:", bg="lightgray")
msg_label.config(font=("Courier", 18))
msg_label.pack(padx=20, pady=5)

input_area = tk.Text(chatWindow, height=1, width=50)
input_area.pack(padx=20, pady=5)

send_message_button = tk.Button(chatWindow, text="Send", command=send_message)
send_message_button.config(font=("Courier", 18))
send_message_button.pack(padx=20, pady=5)

gui_rendered = True
window.mainloop()