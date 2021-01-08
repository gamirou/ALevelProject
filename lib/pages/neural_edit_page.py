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
            },
            "button_add": {
                "text": "Add hidden layer",
                "pos": [10, 0, 1, 2],
                "command": "add_conv_layer"
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
            },
            "button_add": {
                "text": "Add hidden layer",
                "pos": [10, 0, 1, 2],
                "command": "add_fully_layer"
            }
        },
        "frame_output": {
            "label_title": {
                "text": "Optimiser and finishing touches",
                "pos": [0, 0, 1, 2]
            },
            "label_optimizer": {
                "text": "Optimiser",
                "pos": [1, 0, 1, 1]
            },
            "combo_optimizer": {
                "options": ["rmsprop", "adam", "sgd"],
                "text": "rmsprop",
                "pos": [1, 1, 1, 1]
            },
            "label_learning_rate": {
                "text": "Learning rate",
                "pos": [2, 0, 1, 1]
            },
            "entry_learning_rate": {
                "text": "0.01",
                "pos": [2, 1, 1, 1],
                "validate": "callback_entry_numbers"
            }
        }
    }
    visibility_buttons = {}

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.variables = {
            "learning_rate": tk.StringVar(),
            "optimizer": tk.StringVar() 
        }

        # Edit layers
        # padding and stride and all that shize
        self.widgets["frame_conv"] = [ttk.Frame(self, width=100, height=200), 0, 0, 2, 2]
        self.widgets["frame_fully"] = [ttk.Frame(self, width=100, height=200), 0, 2, 2, 2]
        self.widgets["frame_output"] = [ttk.Frame(self, width=100, height=200), 4, 0, 2, 4]

        arrow_left = tk.Button(
            self, text="Back", image=self.parent.file_storage["arrow_left.png"], 
            width=100, height=60, command=self.go_back
        )
        arrow_left.grid(row=10, column=0)

        self.add_hidden_buttons()
        for key, lst in self.widgets.items():
            lst[0].grid(row=lst[1], column=lst[2], rowspan=lst[3], columnspan=lst[4])
            self.render_inner(key, lst)

    def go_back(self):
        # Compile the model
        self.current_network.learning_rate = float(self.variables["learning_rate"].get())
        self.current_network.optimizer = self.variables["optimizer"].get()
        self.parent.back_page()

    def fetch_network(self, network):
        self.current_network = network
        self.configure_buttons()
    
    def add_conv_layer(self):
        if len(self.current_network.layers["convolutional"]) < (self.MAX_LAYERS * 2):
            conv = Conv2D(32, (5,5), activation='relu')
            maxpool = MaxPooling2D(pool_size=(2,2))
            self.visibility["frame_conv"].show_next()
            self.current_network.layers["convolutional"].append(conv)
            self.current_network.layers["convolutional"].append(maxpool)
        else:
            Log.w(self.TAG, "Limit of convolutional layers reached")

    def add_fully_layer(self):
        if len(self.current_network.layers["fully-connected"]) < self.MAX_LAYERS:
            dense = Dense(200, activation='relu')
            dropout = Dropout(0.5)
            index = self.visibility["frame_fully"].show_next()
            self.current_network.layers["fully-connected"].append(dense)
            self.current_network.layers["dropout"][index] = dropout
        else:
            Log.w(self.TAG, "Limit of fully connected layers reached")

    def add_hidden_buttons(self):
        self.visibility["frame_conv"] = VisibilityButtons([False, False, False, False])
        self.visibility["frame_fully"] = VisibilityButtons([False, False, False, False])

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
                widget_name = inner_key.replace("entry_", "")
                print(eval(value["text"]))
                try:
                    default_value = eval(value["text"])
                except:
                    default_value = value["text"]
                
                self.variables[widget_name].set(default_value)
                inner_dict[inner_key]["textvariable"] = self.variables[widget_name]

                if "validate" in inner_dict[inner_key].keys():
                    validate = value.pop("validate", None)
                    vcmd = (frame.register(getattr(self, validate)))
                    widget = tk.Entry(frame, validate='key', validatecommand=(vcmd, '%d', '%P', '%S'), cnf=value)
                    inner_dict[inner_key]["widget"] = widget
                else:
                    inner_dict[inner_key]["widget"] = tk.Entry(frame, cnf=inner_dict[inner_key])
            
            elif "combo" in inner_key:
                options = inner_dict[inner_key]["options"]
                widget = ttk.Combobox(frame, state='readonly', value=options)

                try:
                    default_value = eval(inner_dict[inner_key]["text"])
                    index = options.index(default_value)
                except:
                    index = 0
                
                self.variables[inner_key.replace("combo_", "")].set(value["text"])

                widget.current(index)
                inner_dict[inner_key]["widget"] = widget

            # Only show if it is a layer
            if not is_hidden:
                inner_dict[inner_key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def open_hidden_layer(self, key=0, layer_type=None):
        if layer_type == None:
            layer_type = CONVOLUTIONAL
        Log.i(self.TAG + "/open_hidden_layer", f"Key: {key} = Value: {layer_type}")

        # get the layers
        Log.w("ABC",self.current_network.layers)
        all_layers = self.current_network.layers[layer_type]
        if layer_type == CONVOLUTIONAL:
            index = key * 2
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

        self.layer_window = LayerWindow(self, layer_type, layers, key > 1)
        self.layer_window.title("Edit Layer")
        self.layer_window.grab_set()

    def add_dropout(self, fully_layer, layer):
        index = self.current_network.layers['fully-connected'].index(fully_layer)
        self.current_network.layers['dropout'][index] = layer

    def delete_dropout(self, layer):
        index = self.current_network.layers['dropout'].index(layer)
        self.current_network.layers['dropout'][index] = None

    def delete_layer(self, layer_type, layers):
        if layer_type == CONVOLUTIONAL:
            for layer in layers:
                self.current_network.layers['convolutional'].remove(layer)
            
            self.visibility['frame_conv'].hide_last_visible()
            # self.visibility["frame_conv"][-1] = False
        else:
            self.current_network.layers["fully-connected"].remove(layers[0])
            if layers[1] != None:
                self.delete_dropout(layers[1])

            self.visibility['frame_fully'].hide_last_visible()

    def callback_entry_numbers(self, action, value_if_allowed, text):
        if action=='1' :
            if text in '0123456789.':
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True

    def configure_buttons(self):
        # Make buttons visible based on the number of layers
        # Bug here as well
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