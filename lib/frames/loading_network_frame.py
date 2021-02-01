import tkinter as tk
from ..utils.log import Log
from ..utils.utils import resize_image, DELETE
from ..frames.pop_up_confirm import PopUpConfirm
class LoadingNetworkFrame(tk.Frame):

    TAG = "LoadingNetworkFrame"
    
    def __init__(self, master=None, network=None, file_storage=None, page=None, cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)

        self.widgets = []
        self.file_storage = file_storage
        self.network = network
        self.page = page

        brain_image = self.file_storage['clipart_brain.jpg']
      
        self.widgets.append(tk.Label(self, image=brain_image, bg="#ffffff"))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Name: {network.name}", bg="#ffffff"))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Description: {network.description}", bg="#ffffff"))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Date created: {network.date}", bg="#ffffff"))
        
        for widget in self.widgets:
            widget.pack()
            widget.bind('<Button-1>', self.load_network)

        self.bind('<Button-1>', self.load_network)

    def load_network(self, event):
        self.page.parent.go_to_neural_page(self.network.network_id)