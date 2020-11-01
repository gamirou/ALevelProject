import tkinter as tk

class Page(tk.Frame):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def show(self):
        self.lift()