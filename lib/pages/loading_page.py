import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..utils.log import Log
from ..frames.loading_network_frame import LoadingNetworkFrame

class LoadingPage(Page):

    TAG = "LoadingPage"

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.frames = []
        self.file_storage = self.parent.file_storage
        # tk.Label(self, text="Loading Networks").pack()

        # Main frame
        self.canvas_frame = tk.Frame(self)
        self.canvas_frame.pack(fill=tk.BOTH, expand=1)

        # Canvas
        canvas = tk.Canvas(self.canvas_frame, bg="#ff0000")
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        self.inside_frame = tk.Frame(canvas, bg="#00ff00", width=600, height=600)
        canvas.create_window((0,0), window=self.inside_frame, anchor="nw")

        # TODO: Center inside_frame
        # tk.Label(inside_frame, text="Hello World", fg="#0000ff").pack()
        self.load_networks(self.file_storage.saved_networks)

    def load_networks(self, networks):
        self.frames = []
        index = 0
        for network in networks.values():
            self.frames.append(LoadingNetworkFrame(
                self.inside_frame, bg="#ffffff", network=network, file_storage=self.file_storage, page=self
            ).grid(row=0, column=index, pady=20, padx=20))
            index += 1

        arrow_left = tk.Button(
            self.canvas_frame, text="Back", image=self.file_storage["arrow_left.png"], 
            width=100, height=60, command=self.parent.back_page
        )
        arrow_left.pack()