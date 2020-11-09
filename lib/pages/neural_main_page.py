import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..utils.log import Log

class NeuralMainPage(Page):

    TAG = "NeuralMainPage"

    WELCOME_TEXT = "Hello my friend! My name is 0! My description says: 1!"
    RESULT_TEXT = "Result: "
    ACCURACY_TEXT = "Accuracy: "

    isTraining = False

    widgets = {
        # will use grid system
        # "key": [label, x, y, rowspan, colspan]
    }

    inner_widgets = {
        "frame_input": {
            "label_data": {
                "text": "Data"
            },
            "label_description": {
                "text": "The training data needs to be 36x36 pixels",
                "wraplength": 100
            },
            "label_example_image": {
                "text": "Sample image",
                "image": "image_placeholder.png", # change it self.storage['file_name']
            }
        },
        "frame_process": {
            "label_network": {
                "text": "Network"    
            },
            "button_depth": {
                "text": "Click here to see the network in more details",
                "wraplength": 100,
                "command": "go_to_edit"
            },
            "label_details": {
                "text": "Details"
            },
            "label_values": {
                "text": "So blah blah"
            }
        },
        "frame_output": {
            "label_output": {
                "text": "Output"    
            },
            "label_output_image": {
                "text": "Output image",
                "image": "image_placeholder.png",
                "wraplength": 100
            },
            "label_result": {
                "text": "Result: "
            },
            "label_accuracy": {
                "text": "Accuracy: "
            },
            "button_yes": {
                "text": "YES"
            },
            "button_no": {
                "text": "NO"
            }
        }
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        # TODO: Work on design
        self.file_storage = self.parent.file_storage
        # add column span to array
        self.widgets["label_name"] = [tk.Label(self, text=self.WELCOME_TEXT, bg="#00ff00"), 0, 1, 1, 4]
        # FRAMES THAT HAVE INPUT PROCESS AND OUTPUT

        self.init_inner()

        self.style = ttk.Style()
        self.style.configure("BW.TLabel", background="red")

        self.widgets["frame_input"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 0, 1, 2]
        self.widgets["frame_process"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 2, 1, 2]
        self.widgets["frame_output"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 4, 1, 2]

        self.widgets["button_add_data"] = [ttk.Button(self, text="ADD TEST DATA", command=self.add_data), 2, 0, 1, 1]
        self.widgets["button_pause_train"] = [ttk.Button(self, text="TRAIN", command=self.pause_train), 2, 3, 1, 1]
        self.widgets["button_save"] = [ttk.Button(self, text="SAVE", command=self.save_network), 2, 4, 1, 1]

        for key, lst in self.widgets.items():
            lst[0].grid(row=lst[1], column=lst[2], rowspan=lst[3], columnspan=lst[4])
            if "frame" in key:
                self.render_inner(key, lst)

    def render_inner(self, key, lst):
        frame = lst[0]
        inner_dict = self.inner_widgets[key]

        for key, value in inner_dict.items():
            if "label" in key:
                inner_dict[key]["widget"] = tk.Label(frame, cnf=inner_dict[key])
            elif "button" in key:
                inner_dict[key]["widget"] = tk.Button(frame, cnf=inner_dict[key])

            inner_dict[key]["widget"].pack()

    def fetch_network(self, network):
        # this bit will happen when page is opened
        self.current_network = network
        # show the rest of the bits
        text = self.WELCOME_TEXT.replace("0", network.name)
        text = text.replace("1", network.description)
        self.widgets["label_name"][0]["text"] = text

        if self.current_network.model == None:
            self.current_network.build_model()
            Log.i(self.TAG, "Click the button to edit your network")
        else:
            self.current_network.get_layers_from_model()
        
        # check if compiled

    def init_inner(self):
        for frame_value in self.inner_widgets.values():
            # frame_value - 3 frames
            for widget_key, widget in frame_value.items():
                # every widget
                if "button" in widget_key:
                    # button widgets
                    if "command" in widget.keys():
                        widget["command"] = getattr(self, widget["command"])
                elif "label" in widget_key:
                    if "image" in widget.keys():
                        widget["image"] = self.file_storage[widget["image"]]

    def go_to_edit(self):
        if self.isTraining:
            Log.i(self.TAG, "You cannot enter the page when training data")
            return

        self.parent.update_page("NeuralEditPage")
        self.parent.pages["NeuralEditPage"].fetch_network(self.current_network)

    # Buttons
    def add_data(self):
        # self.go_to_edit()
        pass

    def pause_train(self):
        if self.isTraining:
            # Pause
            pass
        else:
            # Train the model
            pass

    def save_network(self):
        # TODO: Save it
        # code to save it
        # buggy - adds convolutional layers for some reason
        if len(self.current_network.model.layers) == 0:
            self.current_network.add_layers_to_model()
        self.file_storage.save_network(self.current_network)
        self.parent.back_page()