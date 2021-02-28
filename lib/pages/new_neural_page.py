import tkinter as tk
import uuid
from ..page import Page
from ..utils.utils import *

class NewNeuralPage(Page):
    
    entries = {}
    fancy_description = """
    It is very easy and simple to create a new network. Type in the name of your network and you could
    add some words about it, describe it :). Once you finished, click 'Create New Network' and you're done.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        fonts = self.parent.file_storage.fonts

        # Top frame
        top_frame = tk.Frame(self, bg="#ff0")
        tk.Label(
            top_frame, text="Create a new artificial brain",
            bg="#fff", font=fonts["bold medium"]
        ).pack(side=tk.TOP, fill=tk.X, expand=True)
        tk.Label(
            top_frame, text=self.fancy_description,
            bg="#fff", font=fonts["x-small"]
        ).pack(side=tk.TOP, fill=tk.X, expand=True)

        # Input middle frame
        middle_frame = tk.Frame(self, bg="#fff")
        middle_frame.rowconfigure(0, weight=1)
        middle_frame.columnconfigure(0, weight=1)
        middle_frame.rowconfigure(1, weight=1)
        middle_frame.columnconfigure(1, weight=1)
        tk.Label(
            middle_frame, text="Name: ", 
            bg="#fff", font=fonts["small"]
        ).grid(row=0, column=0)
        tk.Label(
            middle_frame, text="Description: ",
            bg="#fff", font=fonts["small"]
        ).grid(row=1, column=0)
        self.entries["name"] = tk.Entry(middle_frame)
        self.entries["description"] = tk.Text(middle_frame, width=40, height=10, font=fonts["x-small"])
        self.entries["name"].grid(row=0, column=1)
        self.entries["description"].grid(row=1, column=1, ipady=10)

        # Footer
        bottom_frame = tk.Frame(self, bg="#fff")
        arrow_left = tk.Button(
            bottom_frame, text="Back", image=self.parent.file_storage["arrow_left.png"], 
            width=ARROW_WIDTH_IMAGE, height=ARROW_HEIGHT_IMAGE, command=self.parent.back_page
        )
        create_network_button = tk.Button(
            bottom_frame, text="Create Network", width=ARROW_WIDTH_CHARS, 
            height=ARROW_HEIGHT_CHARS, command=self.create_network
        )
        arrow_left.pack(side=tk.LEFT)
        create_network_button.pack(side=tk.RIGHT)

        # Pack the frames
        top_frame.pack(side=tk.TOP, anchor=tk.N, fill=tk.X)
        middle_frame.pack(expand=True, anchor=tk.CENTER, fill=tk.BOTH)
        bottom_frame.pack(side=tk.BOTTOM, anchor=tk.S, fill=tk.X)

    def create_network(self):
        name = self.entries["name"].get()
        description = self.entries["description"].get("1.0", tk.END)

        if name == "" or description == "":
            self.parent.notify("The fields are mandatory")
            return
        
        description = description.replace("\n", "")
        values = "{},{},{}".format(name, description, False)
        text = "name,description,is_trained,date\n" + values + "," + today()
        neural_id = str(uuid.uuid4())

        # Create the directory and file
        create_file("saved/" + neural_id, "model_info.txt", text)
        self.parent.add_network(neural_id)
        self.parent.go_to_neural_page(neural_id)