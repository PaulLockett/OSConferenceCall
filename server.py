from serverlib import *
import tkinter as tk
import socket
import threading

 
local_ip_address = socket.gethostbyname(socket.gethostname())

server = StreamingServer(local_ip_address, 9999)
receiver = AudioReceiver(local_ip_address, 8888)

def start_listening():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t1.start()
    t2.start()

window = tk.Tk()
window.title("Server")
window.geometry("300x200")

label_tartget_ip = tk.Label(window, text="Target IP: ")
label_tartget_ip.pack()

text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()

btn_listen = tk.Button(window, text="Start Listening", width=50, command=start_listening)
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_chat = tk.Button(window, text="Start Chat", width=50)
btn_chat.pack(anchor=tk.CENTER, expand=True)

window.mainloop()