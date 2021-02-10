import tkinter as tk
import time
import threading

class NotificationHeader(tk.Frame):

    def __init__(self, master=None, font=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        self.text = tk.Label(self, text="", font=font, bg='#78f542')
        self.is_finished = False
        self.text.pack()

    def show(self, text):
        self.text.config(text=text)
        self.pack(side=tk.TOP, fill=tk.X)
        threading.Timer(6, self.hide).start()

    def hide(self):
        self.is_finished = True