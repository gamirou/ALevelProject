import tkinter as tk
from tkinter import ttk
from ..page import Page
from ..frames.pop_up_confirm import PopUpConfirm
from ..pages.layer_window import LayerWindow
from ..frames.tooltip import ToolTip
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED, DROPOUT, BUILD_MODEL, RESET_ARCHITECTURE
from ..utils.visibility_buttons import VisibilityButtons
from keras.layers import Conv2D, Flatten, MaxPooling2D, Dense, Dropout
import time
import copy
import random

class NeuralEditPage(Page):

    MAX_LAYERS = 4
    visibility = {}
    frame_widgets = {
        "frame_conv": {
            "row": 0,
            "column": 0,
            "rowspan": 1,
            "columnspan": 1
        },
        "frame_fully": {
            "row": 0,
            "column": 1,
            "rowspan": 1,
            "columnspan": 1
        },
        "frame_output": {
            "row": 1,
            "column": 0,
            "rowspan": 1,
            "columnspan": 2
        }
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)

        self.file_storage = self.parent.file_storage
        self.tooltip = self.parent.app.active_tooltip
        self.variables = {
            "learning_rate": tk.StringVar(),
            "optimizer": tk.StringVar() 
        }

        self.widgets = self.file_storage.widgets["NepMainWidgets"]
        self.inner_widgets = self.file_storage.widgets[self.__class__.__name__]

        self.add_hidden_buttons()
        self.render_main_widgets()

    def render_main_widgets(self, parent_widget=None, widgets=None):
        if widgets == None:
            widgets = self.widgets

        for key in widgets:
            text = widgets[key].pop("text", None)
            font = self.get_font(widgets[key])
            if "command" in widgets[key].keys():
                command = getattr(self, widgets[key].pop("command", None))
                
            image_name = widgets[key].pop("image", None)
            width = widgets[key].pop("width", None)
            height = widgets[key].pop("height", None)

            pack_options = copy.copy(widgets[key])
            if "label" in key:
                widgets[key]["widget"] = tk.Label(self, bg="#fff", text=text, font=font, wraplength=400)
            elif "button" in key:
                widgets[key]["widget"] = tk.Button(
                    self, text=text, font=font, command=command, height=height,
                    image=self.file_storage[image_name], width=width
                )
            else:
                if key == "frame_main":    
                    widgets[key]["widget"] = tk.Frame(self, bg="#fff")
                    for i in range(2):
                        widgets[key]["widget"].rowconfigure(i, weight=1)
                        widgets[key]["widget"].columnconfigure(i, weight=1)
                    self.render_main_widgets(widgets[key]["widget"], self.frame_widgets)
                else:
                    widgets[key]["widget"] = tk.Frame(parent_widget, bg="#fff")
                    self.render_inner(key, widgets[key]["widget"])

            if parent_widget == None:
                widgets[key]["widget"].pack(pack_options)
            else:
                widgets[key]["widget"].grid(pack_options)

    def go_back(self):
        # Compile the model
        new_lr = float(self.variables["learning_rate"].get())
        new_optimiser = self.variables["optimizer"].get()

        if new_lr != self.current_network.learning_rate or new_optimiser != self.current_network.optimizer:
            message_box = PopUpConfirm(
                self, BUILD_MODEL, 
                lambda: self.save_finishing_touches(new_lr, new_optimiser)
            )
        else:
            self.parent.back_page()
    
    def save_finishing_touches(self, new_lr, new_optimiser):
        self.current_network.learning_rate = new_lr
        self.current_network.optimizer = new_optimiser
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
            self.parent.notify("New convolutional layer :)")
        else:
            self.parent.notify("Limit of convolutional layers reached")

    def add_fully_layer(self):
        if len(self.current_network.layers["fully-connected"]) < self.MAX_LAYERS:
            dense = Dense(200, activation='relu')
            dropout = Dropout(0.5)
            index = self.visibility["frame_fully"].show_next()
            self.current_network.layers["fully-connected"].append(dense)
            self.current_network.layers["dropout"][index] = dropout
            self.parent.notify("New fully-connected layer :)")
        else:
            self.parent.notify("Limit of fully connected layers reached")

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

    def render_inner(self, key, frame):
        inner_dict = self.inner_widgets[key]
        
        # Render - document
        for inner_key, value in inner_dict.items():
            frame_with_info = None
            is_hidden = False
            info_term = value.pop("info", None)
            pos = value.pop("pos", None)
            font = self.get_font(inner_dict[inner_key])
            
            # If there is an info button, make a frame that will store both the widget and the button
            if info_term != None:
                parent_frame = tk.Frame(frame, bg='#fff')
            else:
                parent_frame = frame

            if "label" in inner_key:
                inner_dict[inner_key]["widget"] = tk.Label(parent_frame, font=font, cnf=inner_dict[inner_key])
                
            elif "button" in inner_key:
                if "command" in inner_dict[inner_key].keys() and isinstance(inner_dict[inner_key]["command"], str):
                    inner_dict[inner_key]["command"] = getattr(self, inner_dict[inner_key]["command"])
                inner_dict[inner_key]["widget"] = tk.Button(parent_frame, font=font, cnf=inner_dict[inner_key])
                
                # add button to visibility buttons class
                if "hidden" in inner_key:
                    self.visibility[key].add_button(inner_dict[inner_key], pos)
                    is_hidden = True

            elif "entry" in inner_key:
                widget_name = inner_key.replace("entry_", "")
                try:
                    default_value = eval(value["text"])
                except:
                    default_value = value["text"]
                
                self.variables[widget_name].set(default_value)
                inner_dict[inner_key]["textvariable"] = self.variables[widget_name]

                if "validate" in inner_dict[inner_key].keys():
                    validate = value.pop("validate", None)
                    vcmd = (parent_frame.register(getattr(self, validate)))
                    widget = tk.Entry(parent_frame, font=font, validate='key', validatecommand=(vcmd, '%d', '%P', '%S'), cnf=value)
                    inner_dict[inner_key]["widget"] = widget
                else:
                    inner_dict[inner_key]["widget"] = tk.Entry(parent_frame, font=font, cnf=inner_dict[inner_key])
            
            elif "combo" in inner_key:
                options = inner_dict[inner_key]["options"]
                
                try:
                    default_value = eval(inner_dict[inner_key]["text"])
                    index = options.index(default_value)
                except:
                    index = 0
                
                var = self.variables[inner_key.replace("combo_", "")]
                var.set(value["text"])

                widget = ttk.Combobox(parent_frame, textvariable=var , state='readonly', value=options)
                widget.current(index)
                inner_dict[inner_key]["widget"] = widget

            # Only show if it is a layer
            if not is_hidden:
                if info_term is not None:
                    parent_frame.grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])
                    definition = self.file_storage.get_definition_by_term(info_term)
                    info_button = tk.Button(
                        parent_frame, bg='#fff', width=32, height=32, relief='flat',
                        image=self.file_storage['info_button_icon.png']
                    )
                    inner_dict[inner_key]["widget"].pack(side=tk.LEFT)
                    info_button.pack(side=tk.LEFT)
                    self.tooltip.add_widget(info_button, definition)
                else:
                    inner_dict[inner_key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])
                
    def open_hidden_layer(self, key=0, layer_type=None):
        if layer_type == None:
            layer_type = CONVOLUTIONAL

        # get the layers
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

        inputs = None
        if layers[0].name in self.current_network.callback.weights["weights"].keys():
            weights = (
                self.current_network.callback.weights["weights"][layers[0].name],
                self.current_network.callback.weights["biases"][layers[0].name],
            )
            if layer_type == CONVOLUTIONAL:
                inputs = self.current_network.model.inputs
        else:
            weights = ()

        self.layer_window = LayerWindow(self, layer_type, layers, key > 0, weights, inputs=inputs)
        self.layer_window.title("Edit Layer")
        self.layer_window.grab_set()
        if self.parent.app.active_tooltip.active_widget != None:
            self.parent.app.active_tooltip.leave()

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

    def reset_architecture_popup(self):
        message_box = PopUpConfirm(self, RESET_ARCHITECTURE, self.reset_architecture)

    def reset_architecture(self):
        self.current_network.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }
        self.current_network.add_layers_to_model()

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

    def get_font(self, widget_dict):
        font_name = widget_dict.pop("font", None)
        if font_name != None:
            return self.file_storage.fonts[font_name]