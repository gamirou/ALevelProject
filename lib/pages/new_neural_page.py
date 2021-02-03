import tkinter as tk
import uuid
from ..page import Page
from ..utils.log import Log
from ..utils.utils import *

class NewNeuralPage(Page):
    
    TAG = "NewNeuralPage"

    entries = {}    
    fancy_description = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam augue turpis, ornare id aliquam at, 
    tristique vel magna. Mauris ultricies tincidunt libero, ac fermentum velit vestibulum vel. 
    Etiam feugiat, felis in suscipit semper, ex magna scelerisque nulla, dictum commodo orci 
    est sed diam. Morbi finibus arcu nec augue ultrices dapibus. Aenean et placerat lorem. 
    Pellentesque tempor sem arcu, vitae cursus mauris imperdiet at. Praesent vestibulum ex sit amet 
    erat elementum, sed ultrices nisi commodo. Vestibulum sed sem feugiat, tempus nibh nec, faucibus 
    justo. In vulputate aliquet nulla, eget pulvinar nisl pharetra vel. Nam tempus aliquam urna, 
    rutrum tincidunt tortor tincidunt eu. Vestibulum blandit ut est quis maximus. Nullam sagittis 
    rhoncus lectus hendrerit eleifend. Etiam id neque dui. Ut finibus tortor quis justo condimentum, 
    eu sollicitudin massa pretium. Nullam posuere varius urna sit amet volutpat. Nunc ut rhoncus magna, 
    accumsan efficitur justo.
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

        print(name, description)
        if name == "" or description == "":
            Log.w(self.TAG, "The fields are mandatory")
            return
        
        description = description.replace("\n", "")
        values = "{},{},{}".format(name, description, False)
        text = "name,description,is_trained,date\n" + values + "," + today()
        neural_id = str(uuid.uuid4())

        # Create the directory and file
        create_file("saved/" + neural_id, "model_info.txt", text)
        self.parent.add_network(neural_id)
        self.parent.go_to_neural_page(neural_id)

    # def create_network(self):
    #     # Lst is a boolean list
    #     # true = value is empty or key = default
    #     # if all three are false, the network can be created
    #     # if any are true, it will not allow the user to enter any more info
    #     values_changed = [value.get() == "" for key, value in self.variables.items()]
    #     if any(values_changed):
    #         # TODO: Change it to message shown on window
    #         Log.w(self.TAG, "The fields are mandatory")
    #         return

    #     # TODO: Do something about new lines in description

    #     # Data will be stored in a directory
    #     # dir name = uuid 
    #     # files - model_info.txt (name, description and date)
    #     #       - model.h5 (actual model)
    #     #       - model_metrics.json (nice details in JSON format)
    #     desc = self.variables["description"].get()
    #     desc = desc.replace("\n", " ")
    #     values = "{},{},{}".format(
    #         self.variables["name"].get(),
    #         desc, False
    #     )
    #     text = "name,description,is_trained,date\n" + values + "," + today()
    #     neural_id = str(uuid.uuid4())

    #     # Create the directory and file
    #     create_file("saved/" + neural_id, "model_info.txt", text)
    #     self.parent.add_network(neural_id)
    #     self.parent.go_to_neural_page(neural_id)