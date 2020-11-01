import tkinter as tk
import uuid
from ..page import Page
from ..utils.log import Log
from ..utils.utils import *

class NewNeuralPage(Page):
    
    TAG = "NewNeuralPage"

    entries = {}
    variables = {}

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Labels
        tk.Label(self, text="Name: ").grid(row=0, column=0)
        tk.Label(self, text="Description: ").grid(row=1, column=0)
        self.variables["name"] = tk.StringVar()
        self.variables["description"] = tk.StringVar()

        # Entries
        self.entries["name"] = tk.Entry(self, text="name", textvariable=self.variables["name"])
        self.entries["description"] = tk.Entry(self, text="description", textvariable=self.variables["description"])
        
        # Grid them
        self.entries["name"].grid(row=0, column=1)
        self.entries["description"].grid(row=1, column=1)

        arrow_left = tk.Button(
            self, text="Back", image=self.parent.file_storage["arrow_left.png"], width=100, height=60,
            command=self.parent.back_page
        )
        arrow_left.grid(row=3, column=0)

        create_network_button = tk.Button(self, text="Create Network", width=20, height=4, command=self.create_network)
        create_network_button.grid(row=3, column=1)

    def create_network(self):
        # Lst is a boolean list
        # true = value is empty or key = default
        # if all three are false, the network can be created
        # if any are true, it will not allow the user to enter any more info
        lst = [value.get() == "" for key, value in self.variables.items()]
        if any(lst):
            # TODO: Change it to message shown on window
            Log.w(self.TAG, "The fields are mandatory")
            return

        # TODO: Do something about new lines in description

        # Data will be stored in a directory
        # dir name = uuid 
        # files - model_info.txt (name, description and date)
        #       - model.h5 (actual model)
        #       - model.json (nice details in JSON format)
        desc = self.variables["description"].get()
        desc = desc.replace("\n", " ")
        values = "{},{}".format(
            self.variables["name"].get(),
            desc
        )
        text = "name,description,date\n" + values + "," + today()
        neural_id = str(uuid.uuid4())

        # Create the directory and file
        # default values represent 
        create_file("saved/" + neural_id, "model_info.txt", text)
        self.parent.add_network(neural_id)
        self.parent.go_to_neural_page(neural_id)