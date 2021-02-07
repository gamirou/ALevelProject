import tkinter as tk
from tkinter import scrolledtext

class ResizeableScrolledText(scrolledtext.ScrolledText):
    def __init__(self, master=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        # canvas = tk.Canvas(self)
        # scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        # scrollable_frame = tk.Frame(canvas)
        # scrollable_frame.bind(
        #     "<Configure>",
        #     lambda e: canvas.configure(
        #         scrollregion=canvas.bbox("all")
        #     )
        # )
        # canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        # canvas.configure(yscrollcommand=scrollbar.set)

        # canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # self.label = tk.Label(scrollable_frame, cnf=label_cnf)
        # self.label.pack()