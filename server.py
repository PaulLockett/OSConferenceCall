from serverlib import *
import tkinter as tk
import tkinter.simpledialog as tkSimpleDialog
import socket
import threading


def start_server():
    t1 = threading.Thread(target=server.start_server)
    t2 = threading.Thread(target=receiver.start_server)
    t3 = threading.Thread(target=chatRoom.start)
    t1.start()
    t2.start()
    t3.start()

def stop_server():
    server.stop_server()
    receiver.stop_server()
    chatRoom.stop()
    exit()

window = tk.Tk()
window.withdraw()

server_address = tkSimpleDialog.askstring("Server Address", "Enter the server address:")

if server_address is None:
    server_address = socket.gethostbyname(socket.gethostname())

server = StreamingServer(server_address, 9999)
receiver = AudioServer(server_address, 8888)
chatRoom = ChatServer(server_address, 7777)

window.wm_deiconify()

window.title("Server")
window.geometry("300x200")

text_target_ip = tk.Text(window, height=1)
text_target_ip.pack()

btn_listen = tk.Button(window, text="Start Server", width=50, command=start_server)
btn_listen.pack(anchor=tk.CENTER, expand=True)

btn_stop = tk.Button(window, text="Stop Server", width=50, command=stop_server)
btn_stop.pack(anchor=tk.CENTER, expand=True)

window.mainloop()