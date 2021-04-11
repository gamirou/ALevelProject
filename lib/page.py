import tkinter as tk

class Page(tk.Frame):

    """
    Subclass of tkinter Frame that can be hidden on command
    """

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

    def show(self):
        self.lift()