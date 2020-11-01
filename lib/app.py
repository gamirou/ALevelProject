import tkinter as tk
from .main_view import MainView
from .file_storage import FileStorage
from .utils.log import Log

class App:

    TAG = "App"

    def __init__(self):
        self.title = "Image Recognition for all"
        self.root = tk.Tk()
        self.root.title(self.title)

        # Cache images
        self.file_storage = FileStorage()

        # MainView is a container for all pages
        self.view = MainView(self.root, self.file_storage)
        self.view.pack(side="top", fill="both", expand=True)
        self.root.wm_geometry("600x600")

    def update(self):
        self.root.mainloop()