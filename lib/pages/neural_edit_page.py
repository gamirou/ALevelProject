import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..pages.layer_window import LayerWindow
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED, DROPOUT
from ..utils.log import Log
from ..utils.visibility_buttons import VisibilityButtons
import time

import warnings
warnings.filterwarnings("ignore")
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout

import random

class NeuralEditPage(Page):

    TAG = "NeuralEditPage"

    MAX_LAYERS = 4
    CONVOLUTIONAL = "convolutional"
    FULLY_CONNECTED = "fully-connected"
    STATE = ""
    # states = ["EDIT", "COMPILED", "TRAINED"]

    visibility = {}

    # same as NeuralMainPage
    widgets = {}
    inner_widgets = {
        "frame_conv": {
            "label_title": {
                "text": "Convolutional layers",
                "pos": [0, 0, 1, 2]
            },
            "label_input": {
                "text": "Input layer",
                "pos": [1, 0, 1, 1]
            },
            "button_input": {
                "text": "Click to edit input layer",
                "pos": [1, 1, 1, 1],
                "command": "open_hidden_layer"#(0, 'convolutional')"
            },
            "label_hidden": {
                "text": "Hidden layers: 1-4",
                "pos": [2, 0, 1, 2]
            }
        },
        "frame_fully": {
            "label_title": {
                "text": "Fully-connected layers",
                "pos": [0, 0, 1, 2]
            },
            "label_input": {
                "text": "Input layer: cannot be changed",
                "pos": [1, 0, 1, 1]
            },
            "label_hidden": {
                "text": "Hidden layers: 1-4",
                "pos": [2, 0, 1, 1]
            }
        },
        "frame_output": {}
    }
    visibility_buttons = {}

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        # Edit layers
        # padding and stride and all that shize
        self.widgets["frame_conv"] = [ttk.Frame(self, width=100, height=200), 0, 0, 2, 2]
        self.widgets["frame_fully"] = [ttk.Frame(self, width=100, height=200), 0, 2, 2, 2]
        self.widgets["frame_output"] = [ttk.Frame(self, width=100, height=200), 2, 0, 3, 2]

        arrow_left = tk.Button(
            self, text="Back", image=self.parent.file_storage["arrow_left.png"], 
            width=100, height=60, command=self.parent.back_page
        )
        arrow_left.grid(row=5, column=0)

        self.add_hidden_buttons()
        for key, lst in self.widgets.items():
            lst[0].grid(row=lst[1], column=lst[2], rowspan=lst[3], columnspan=lst[4])
            self.render_inner(key, lst)

    def go_back(self):
        self.parent.back_page()

    def fetch_network(self, network):
        self.current_network = network
        self.configure_buttons()
    
    def add_hidden_buttons(self):
        self.visibility["frame_conv"] = VisibilityButtons([True, True, True, True])
        self.visibility["frame_fully"] = VisibilityButtons([True, True, True, True])

        # Add the hidden buttons
        for i in range(1, self.MAX_LAYERS+1):
            conv_widget = {
                "text": f"Convolutional hidden layer {i}",
                "pos": [2+i, 0, 1, 2],
                "command": lambda index=i: self.open_hidden_layer(index, CONVOLUTIONAL)
            }
            fully_widget = {
                "text": f"Fully-connected hidden layer {i}",
                "pos": [2+i, 0, 1, 2],
                # TODO: Function not called
                "command": lambda index=i: self.open_hidden_layer(index, FULLY_CONNECTED)
            }

            # Widgets added
            self.inner_widgets["frame_conv"][f"button_hidden_{i}"] = conv_widget
            self.inner_widgets["frame_fully"][f"button_hidden_{i}"] = fully_widget

    def render_inner(self, key, lst):
        frame = lst[0]
        inner_dict = self.inner_widgets[key]

        # Render - document
        for inner_key, value in inner_dict.items():
            is_hidden = False
            pos = value.pop("pos", None)
            if "label" in inner_key:
                inner_dict[inner_key]["widget"] = tk.Label(frame, cnf=inner_dict[inner_key])
                
            elif "button" in inner_key:
                if "command" in inner_dict[inner_key].keys() and isinstance(inner_dict[inner_key]["command"], str):
                    inner_dict[inner_key]["command"] = getattr(self, inner_dict[inner_key]["command"])
                inner_dict[inner_key]["widget"] = tk.Button(frame, cnf=inner_dict[inner_key])
                
                # add button to visibility buttons class
                if "hidden" in inner_key:
                    self.visibility[key].add_button(inner_dict[inner_key], pos)
                    is_hidden = True

            elif "entry" in inner_key:
                inner_dict[inner_key]["widget"] = tk.Entry(frame, cnf=inner_dict[inner_key])
                
            # Only show if it is a layer
            if not is_hidden:
                inner_dict[inner_key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def open_hidden_layer(self, key=0, layer_type=None):
        if layer_type == None:
            layer_type = CONVOLUTIONAL
        Log.i(self.TAG + "/open_hidden_layer", f"Key: {key} = Value: {layer_type}")

        # get the layers
        all_layers = self.current_network.layers[layer_type]
        if layer_type == CONVOLUTIONAL:
            index = key // 2
            convolutional = all_layers[index]
            pooling = all_layers[index + 1]
            layers = (convolutional, pooling)
        else:
            index = key - 1
            dense = all_layers[index]
            dropout_layers = self.current_network.layers[DROPOUT]
            dropout = None
            if index < len(dropout_layers):
                dropout = dropout_layers[index]
            layers = (dense, dropout)

        window = LayerWindow(self.parent.parent, layer_type, layers)

    def configure_buttons(self):
        # Make buttons visible based on the number of layers
        for layer_type, layers in self.current_network.layers.items():
            index = 0
            for layer in layers:
                # ignore if it's input or output layers
                if isinstance(layer, Conv2D) and layers.index(layer) > 0:
                    self.visibility["frame_conv"][index] = True
                    index += 1
                elif isinstance(layer, Dense) and layers.index(layer) < len(layers) - 1 :
                    self.visibility["frame_fully"][index] = True
                    index += 1

        # print(self.visibility_buttons)