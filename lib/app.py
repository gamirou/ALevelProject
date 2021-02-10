import tkinter as tk
import time
from tkinter import ttk
from .main_view import MainView
from .file_storage import FileStorage
from .frames.progress_bar_footer import ProgressBarFooter
from .frames.notification_header import NotificationHeader
from .utils.log import Log
import matplotlib.animation as animation
from .utils.utils import DETERMINATE, INDETERMINATE, get_main_path
class App:

    TAG = "App"

    def __init__(self):
        self.title = "Image Classification for all"
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.minsize(700, 700)
        # self.root.iconbitmap(get_main_path('assets', 'favicon.ico'))

        # Update loop variables        
        self.is_running = True
        self.is_loaded = False
        self.thread_output = []

        # Cache images
        self.file_storage = FileStorage(self)

        # Notification header
        self.notification_header = NotificationHeader(
            self.root, font=self.file_storage.fonts["bold small"], bg="#78f542",
            highlightbackground="black", highlightthickness=1
        )

        # Progress bar
        self.progress_footer = ProgressBarFooter(
            self.root, font=self.file_storage.fonts["bold small"], length=300,
            bg="#f2e463", highlightbackground="black", highlightthickness=1
        )
        self.progress_footer.start(mode=INDETERMINATE)

        self.init_main_view()
        self.progress_footer.pack(side=tk.BOTTOM, fill=tk.X)

    def init_main_view(self):
        # MainView is a container for all pages
        self.view = MainView(self.root, self, self.file_storage, 
                width=self.root.winfo_width(), height=self.root.winfo_height(), bg="#00ff00")
        self.view.pack(side="top", fill="both", expand=True)

    def update(self):
        while self.is_running:
            # When loading dataset (progress bar is visible on start)
            if not self.file_storage.is_loading and not self.is_loaded:
                self.progress_footer.stop()
                self.is_loaded = True

            # Only if mode is determinate
            if self.progress_footer.value_changed and self.progress_footer.mode == DETERMINATE:
                self.progress_footer.show_updated_progress()
                self.progress_footer.value_changed = False

            # Stop progress bar
            if self.progress_footer.is_finished:
                self.progress_footer.stop()
                self.progress_footer.is_finished = False

            # Do stuff with the values from threads in main tkinter thread
            for val in self.thread_output:
                val[1](val[0])
                self.thread_output.remove(val)

            # Hide the notification header panel thing
            if self.notification_header.is_finished:
                self.notification_header.pack_forget()
                self.notification_header.is_finished = False

            self.root.update()