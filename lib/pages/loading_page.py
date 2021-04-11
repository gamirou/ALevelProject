import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..frames.loading_network_frame import LoadingNetworkFrame
from ..utils.utils import ARROW_WIDTH_IMAGE, ARROW_HEIGHT_IMAGE

class LoadingPage(Page):

    fancy_description = """
    Can you see those little boxes? If you can't, you will have to go back to create a new network.
    If you can, each box is one of your networks and if you click them you will be able to play
    around with your chosen network. I've also added a nice brain image in there, it's nice isn't it?
    I like it, do you like it?
    """

    # self.index -> number of frames needed for networks

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.frames = []
        self.file_storage = self.parent.file_storage
        # tk.Label(self, text="Loading Networks").pack()

        # Main frame
        self.canvas_frame = tk.Frame(self, bg="#fff")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        # Title and description
        tk.Label(
            self.canvas_frame, text="Load a neural network",
            font=self.file_storage.fonts["bold medium"], bg="#fff"
        ).pack(side=tk.TOP, anchor=tk.N, fill=tk.X)
        tk.Label(
            self.canvas_frame, text=self.fancy_description,
            font=self.file_storage.fonts["x-small"], bg="#fff"
        ).pack(side=tk.TOP, anchor=tk.N, fill=tk.X)

        # Canvas
        canvas = tk.Canvas(self.canvas_frame, bg="#fff")
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        self.inside_frame = tk.Frame(canvas, bg="#fff", width=600, height=600)
        canvas.create_window((0,0), window=self.inside_frame, anchor=tk.NW)
        
        self.arrow_left = tk.Button(
            self.canvas_frame, text="Back", image=self.file_storage["arrow_left.png"], 
            width=ARROW_WIDTH_IMAGE, height=ARROW_HEIGHT_IMAGE, command=self.parent.back_page
        )
        self.arrow_left.pack(side=tk.LEFT)
        self.load_networks(self.file_storage.saved_networks)

    def load_networks(self, networks):
        self.frames = {}
        self.index = 0
        for key in networks:
            self.add_frame(key)

    def add_frame(self, neural_id):
        self.frames[neural_id] = LoadingNetworkFrame(
            self.inside_frame, bg="#ffffff", network=self.file_storage.saved_networks[neural_id], 
            file_storage=self.file_storage, page=self, highlightbackground="black", highlightthickness=1
        )
        self.frames[neural_id].grid(row=0, column=self.index, pady=20, padx=20)
        self.index += 1
    
    def __setitem__(self, key, item):
        self.frames[key] = item

    def __getitem__(self, key):
        return self.frames[key]