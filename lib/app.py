import tkinter as tk
import time
from tkinter import ttk
from .main_view import MainView
from .file_storage import FileStorage
from .utils.log import Log
import matplotlib.animation as animation

class App:

    TAG = "App"

    def __init__(self):
        self.title = "Image Recognition for all"
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.wm_geometry("600x600")

        self.is_running = True
        self.is_loaded = False
        self.graphs = {}

        # Progress bar
        self.progress_frame = tk.Frame(self.root)
        self.progress_text = tk.Label(self.progress_frame, text="Loading dataset...")
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress_text.pack()
        self.progress_bar.pack()
        self.progress_bar.start()

        # Cache images
        self.file_storage = FileStorage(self)
        self.init_main_view()
        self.progress_frame.pack()

    def init_main_view(self):
        # MainView is a container for all pages
        Log.i(self.TAG, "Init Main View")
        self.view = MainView(self.root, self, self.file_storage, 
                width=self.root.winfo_width(), height=self.root.winfo_height(), bg="#00ff00")
        self.view.pack(side="top", fill="both", expand=True)

    def update(self):
        while self.is_running:
            if not self.file_storage.is_loading and not self.is_loaded:
                self.stop_progress()
                self.is_loaded = True
                
            for graph in self.graphs.values():
                ani = animation.FuncAnimation(graph["figure"], graph["animate"], interval=5000)

            self.root.update()

    def stop_progress(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.progress_frame.pack_forget()