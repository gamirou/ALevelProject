import tkinter as tk
from tkinter import ttk

class ScrollableText(tk.Frame):
    def __init__(self, master=None, cnf={}, **kw):
        label_cnf = kw.get('label_cnf', None)
        kw.pop('label_cnf', None)
    
        super().__init__(master=master, cnf={}, **kw)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.label = tk.Label(scrollable_frame, cnf=label_cnf)
        self.label.pack()
    
    def bind(self):
        self.label.bind('<Configure>', lambda e: self.label.config(wraplength=self.winfo_width()))