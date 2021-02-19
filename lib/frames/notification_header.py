import tkinter as tk
import time

class NotificationHeader(tk.Frame):

    def __init__(self, master=None, font=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        self.text = tk.Label(self, text="", font=font, bg='#78f542')
        self.text.pack()

    def show(self, text):
        self.text.config(text=text)
        self.pack(side=tk.TOP, fill=tk.X)
        self.after(5000, self.pack_forget)