import tkinter as tk
from ..utils.log import Log
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED

class LayerWindow(tk.Toplevel):

    TAG = "LayerWindow"

    def __init__(self, master=None, layer_type=None, layers=(), cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.parent = master

        self.conv_widgets = {
            "label_title_1": {
                "text": "Convolutional Layer",
                "pos": [0, 0, 1, 2]
            },
            "label_stride_x": {
                "text": "Stride in the x-axis",
                "pos": [1, 0, 1, 1]
            },
            "entry_stride_x": {
                "text": "self.layers[0].strides[0]",
                "pos": [1, 1, 1, 1]
            },
            # {<keras.layers.convolutional.Conv2D object at 0x000002C41EC35E48>} 
            # {<keras.layers.pooling.MaxPooling2D object at 0x000002C41EE84240>}
            "label_stride_y": {
                "text": "Stride in the y-axis",
                "pos": [2, 0, 1, 1]
            },
            "entry_stride_y": {
                "text": "self.layers[0].strides[1]",
                "pos": [2, 1, 1, 1]
            },
            "label_padding": {
                "text": "Padding",
                "pos": [3, 0, 1, 1]
            },
            "entry_padding": {
                "text": "self.layers[0].padding",
                "pos": [3, 1, 1, 1]
            },
            "label_title_2": {
                "text": "Max Pooling",
                "pos": [4, 0, 1, 2]
            },
            "label_pool_x": {
                "text": "Pool size x-axis",
                "pos": [5, 0, 1, 1]
            },
            "entry_pool_x": {
                "text": "self.layers[1].pool_size[0]",
                "pos": [5, 1, 1, 1]
            },
            "label_pool_y": {
                "text": "Pool size y-axis",
                "pos": [6, 0, 1, 1]
            },
            "entry_pool_y": {
                "text": "self.layers[1].pool_size[1]",
                "pos": [6, 1, 1, 1]
            },
            "save_button": {
                "text": "Save",
                "command": "save_layer",
                "pos": [8, 0, 1, 2]
            }
        }
        self.fully_connected_widgets = {
            "label_title_1": {
                "text": "Main Layer",
                "pos": [0, 0, 1, 2]
            },
            "label_neurons": {
                "text": "Number of neurons: ",
                "pos": [1, 0, 1, 1]
            },
            "entry_neurons": {
                "pos": [1, 1, 1, 1],
                "text": "self.layers[0].units"
            },
            "checkbutton_dropout": {
                "text": "Dropout",
                "pos": [2, 0, 1, 2],
                "variable": tk.IntVar(),
                "command": "open_dropout"
            },
            "label_dropout": {
                "text": "Rate",
                "pos": [3, 0, 1, 1]
            },
            "entry_dropout": {
                "pos": [3, 1, 1, 1]
            },
            "save_button": {
                "text": "Save",
                "command": "save_layer",
                "pos": [4, 0, 1, 2]
            }
        }

        # Variables
        self.variables = {
            # Convolutional
            "stride_x": tk.StringVar(),
            "stride_y": tk.StringVar(),
            "padding": tk.StringVar(),
            "pool_x": tk.StringVar(),
            "pool_y": tk.StringVar(),

            # Fully-connected
            "neurons": tk.StringVar(),
            "dropout": tk.StringVar()
        }

        self.layer_type = layer_type
        self.layers = layers
        self.render_widgets()

    def save_layer(self):    
        values = {key: self.variables[key].get() for key in self.variables}
        if self.validate_values(values):
            if self.layer_type == CONVOLUTIONAL:
                conv = self.layers[0]
                maxpooling = self.layers[1]

                stride = (int(values["stride_x"], 10), int(values["stride_y"], 10))
                pooling = (int(values["pool_x"], 10), int(values["pool_y"], 10))
                conv.strides = stride
                conv.padding = values["padding"]
                maxpooling.pool_size = pooling
            else:
                pass
        else:
            Log.e(self.TAG, "Convolutional layer cannot be saved", "Invalid input")
            return
        
        Log.i(self.TAG, self.layer_type + " layer saved!")
        self.destroy()

    def validate_values(self, values):
        return True

    def open_dropout(self):
        var = self.fully_connected_widgets["checkbutton_dropout"]["variable"]
        entry = self.fully_connected_widgets["entry_dropout"]["widget"]
    
        if var.get():
            entry.config(state='normal')
        else:
            entry.config(state='disabled')

    def render_widgets(self):
        widgets = self.conv_widgets if self.layer_type == CONVOLUTIONAL else self.fully_connected_widgets        

        # Render - document
        for widget_key, value in widgets.items():
            pos = value.pop("pos", None)
            if "label" in widget_key:
                widgets[widget_key]["widget"] = tk.Label(self, cnf=widgets[widget_key])

            elif "checkbutton" in widget_key:
                if "command" in widgets[widget_key].keys() and isinstance(widgets[widget_key]["command"], str):
                    widgets[widget_key]["command"] = getattr(self, widgets[widget_key]["command"])

                self.is_dropout = widgets[widget_key]["variable"]
                if self.layers[1] != None:
                    self.is_dropout.set(1)
                    widgets["entry_dropout"]["text"] = "self.layers[1].rate"
                
                widgets[widget_key]["widget"] = tk.Checkbutton(self, cnf=widgets[widget_key])

            elif "button" in widget_key:
                if "command" in widgets[widget_key].keys() and isinstance(widgets[widget_key]["command"], str):
                    widgets[widget_key]["command"] = getattr(self, widgets[widget_key]["command"])
                widgets[widget_key]["widget"] = tk.Button(self, cnf=widgets[widget_key])
                
            elif "entry" in widget_key:
                widget_name = widget_key.replace("entry_", "")
                try:
                    default_value = eval(widgets[widget_key]["text"])
                    self.variables[widget_name].set(default_value)
                except:
                    default_value = ""
                
                widgets[widget_key]["textvariable"] = self.variables[widget_name]
                widgets[widget_key]["widget"] = tk.Entry(self, cnf=widgets[widget_key])
                # widgets[widget_key]["widget"].delete(0, tk.END)
                # widgets[widget_key]["widget"].insert(0, default_value)

                if widget_key == "entry_dropout":
                    if not self.is_dropout.get():
                        widgets[widget_key]["widget"].config(state='disabled')

            widgets[widget_key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])