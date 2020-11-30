import tkinter as tk
from tkinter import ttk
from .main_view import MainView
from .file_storage import FileStorage
from .utils.log import Log

class App:

    TAG = "App"

    def __init__(self):
        self.title = "Image Recognition for all"
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.wm_geometry("600x600")

        self.progress = ttk.Progressbar(self.root, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progress.pack()
        
        # Cache images
        self.file_storage = FileStorage(self)

    def init_main_view(self):
        # MainView is a container for all pages
        Log.i(self.TAG, "Init Main View")
        self.view = MainView(self.root, self.file_storage)
        self.view.pack(side="top", fill="both", expand=True)

    def update(self):
        self.root.mainloop()