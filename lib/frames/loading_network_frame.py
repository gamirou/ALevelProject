import tkinter as tk
from ..utils.utils import resize_image, DELETE
from ..frames.pop_up_confirm import PopUpConfirm
class LoadingNetworkFrame(tk.Frame):

    TAG = "LoadingNetworkFrame"
    
    def __init__(self, master=None, network=None, file_storage=None, page=None, cnf={}, **kw):
        super().__init__(master=master, cnf=cnf, **kw)

        self.widgets = []
        self.file_storage = file_storage
        self.network = network
        self.page = page

        brain_image = self.file_storage['clipart_brain.jpg']
        font = self.file_storage.fonts["bold x-small"]

        desc = network.description if len(network.description) <= 20 else network.description[:20]
      
        self.widgets.append(tk.Label(self, image=brain_image, bg="#ffffff", font=font))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Name: {network.name}", bg="#ffffff", font=font))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Description: {desc}", bg="#ffffff", font=font))
        self.widgets.append(tk.Label(self, wraplength=150, text=f"Last edited: {network.date}", bg="#ffffff", font=font))
        
        for widget in self.widgets:
            widget.pack()
            widget.bind('<Button-1>', self.load_network)

        self.bind('<Button-1>', self.load_network)

    def load_network(self, event):
        self.page.parent.go_to_neural_page(self.network.network_id)