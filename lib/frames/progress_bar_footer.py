import tkinter as tk
from tkinter import ttk
from ..utils.utils import DETERMINATE, INDETERMINATE, TRAIN

class ProgressBarFooter(tk.Frame):

    """
    A small tkinter box which shows a progress bar on a variety of actions that work on a separate thread.
    There is a special case on training the network when it has to show more information
    """

    def __init__(self, master=None, text="Loading dataset", length=100, font=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)
        self.parent = master
        
        # Optional values
        self.epoch_text = None
        self.is_sub_text = None
        self.metrics_text = None
        
        # Values we need
        self.values = {'progress': -1, 'logs': {}, 'epoch': -1}
        self.text = text
        self.font = font
        self.length = length
        self.progress_bar = None
        self.is_finished = False
        self.value_changed = False
        self.progress_text = tk.Label(self, text=f"{self.text}...", bg="#f2e463", font=self.font)
        self.progress_text.pack()

    """
    Start and show the progress bar
    """
    def start(self, mode, text=None, is_sub_text=None, epochs=1):
        self.mode = mode
        self.is_sub_text = is_sub_text
        if text != None:
            self.text = text
            self.progress_text['text'] = self.text + "..."
        self.pack(side=tk.BOTTOM, fill=tk.X)

        # Subtext (only for training, could be expanded)
        if is_sub_text == TRAIN:
            self.total_epochs = epochs
            self.epoch_text = tk.Label(self, text=f"Epoch 1/{self.total_epochs}", bg="#f2e463", font=self.font)
            self.metrics_text = tk.Label(self, text="Accuracy: 0, Loss: 0", bg="#f2e463", font=self.font)
            self.epoch_text.pack()
            self.metrics_text.pack()

        # Redraw the progress back
        if self.progress_bar == None:
            self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=self.length, mode=mode)
        else:
            self.progress_bar.config(mode=self.mode)
        
        self.progress_bar.pack(pady=20)
        if mode == INDETERMINATE:
            self.progress_bar.start()

    """
    Stop and hide the progress bar
    """
    def stop(self):
        if self.mode == INDETERMINATE:
            self.progress_bar.stop()
        
        if self.is_sub_text == TRAIN:
            self.epoch_text.pack_forget()
            self.metrics_text.pack_forget()

        self.pack_forget()

    """
    Values taken from WeightsCallback. This is called from separate thread
    """
    def update_values(self, values):
        self.value_changed = values['progress'] == self.values['progress']
        self.values = values
    
    """
    Update the GUI based on the values
    """
    def show_updated_progress(self):
        if self.is_sub_text == TRAIN:
            accuracy_perc = round(self.values['logs']['accuracy'] * 100, 3)
            loss_value = round(self.values['logs']['loss']*1, 5)
            self.epoch_text["text"] = f"Epoch {self.values['epoch']}/{self.total_epochs}"
            self.metrics_text["text"] = f"Accuracy: {accuracy_perc}%, Loss: {loss_value}"
        self.progress_bar["value"] = self.values['progress']