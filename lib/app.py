import tkinter as tk
import time
from tkinter import ttk
from .main_view import MainView
from .file_storage import FileStorage
from .frames.progress_bar_footer import ProgressBarFooter
from .frames.notification_header import NotificationHeader
from .frames.pop_up_confirm import PopUpConfirm
from .frames.tooltip import ToolTip
import matplotlib.animation as animation
from .utils.utils import *
class App:

    def __init__(self):
        self.title = "Image Classification for all"
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.minsize(APP_SIZE, APP_SIZE)
        # self.root.iconbitmap(get_main_path('assets', 'favicon.ico'))

        # Update loop variables        
        self.is_running = True
        self.is_loaded = False
        self.thread_output = []
        self.active_tooltip = ToolTip()

        # Close window
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

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
        self.root.bind('<Configure>', self.configure_tooltip)

        while self.is_running:
            # When loading dataset (progress bar is visible on start)
            if not self.file_storage.dataset.is_loading and not self.is_loaded:
                self.progress_footer.stop()
                self.is_loaded = True
                self.notification_header.show('The data has been loaded')

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

            self.root.update()

    def configure_tooltip(self, event=None):
        if self.active_tooltip.top_level != None:
            x = y = 0
            x, y, cx, cy = self.active_tooltip.active_widget.bbox("insert")
            x += self.active_tooltip.active_widget.winfo_rootx() + self.active_tooltip.offset['x']
            y += self.active_tooltip.active_widget.winfo_rooty() + self.active_tooltip.offset['y']
            self.active_tooltip.top_level.geometry(f"+{x}+{y}")
    
    def close_window_and_save_network(self):
        self.view.pages["NeuralMainPage"].save_network()
        self.set_is_running(False)
    
    def set_is_running(self, value):
        self.is_running = value

    def close_window(self):
        if "NeuralMainPage" in self.view.page_stack:
            if not self.view.pages["NeuralMainPage"].is_training:
                message_box = PopUpConfirm(
                    self.view.pages[self.view.current_id], CLOSE_WINDOW, 
                    self.close_window_and_save_network,
                    additional_command=self.set_is_running
                )
            else:
                self.notification_header.show("Network is training")
        else:
            if tk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.is_running = False