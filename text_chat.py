from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.title("Text Chat")


text_chat = Toplevel()

def push():
	myLabel = Label(text_chat, text=e.get())
	myLabel.grid(row=2, column=3)

e = Entry(text_chat, width=35, borderwidth=5)
e.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
b1 = Button(text_chat, text="enter", command=push)
b1.grid(row=1, column=1)



root.mainloop()