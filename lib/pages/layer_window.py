import tkinter as tk
from tkinter import ttk
from ..utils.log import Log
from ..utils.utils import CONVOLUTIONAL, FULLY_CONNECTED, WIDGETS_TYPE, SAVE_BUTTON_POS

import warnings
import copy
warnings.filterwarnings("ignore")
from keras.layers import Dropout

class LayerWindow(tk.Toplevel):

    TAG = "LayerWindow"

    def __init__(self, master=None, layer_type=None, layers=(), can_be_deleted=True, cnf={}, **kw):
        super().__init__(master=master, cnf={}, **kw)
        self.parent = master
        self.can_be_deleted = can_be_deleted

        self.save_button = {
            "text": "Save",
            "command": "save_layer",
            "pos": [4, 1, 1, 1]
        }

        # Variables
        self.variables = {
            # Convolutional
            "filters": tk.StringVar(),
            "kernel_size": tk.StringVar(),
            "stride_x": tk.StringVar(),
            "stride_y": tk.StringVar(),
            "padding": tk.StringVar(),
            "pool": tk.StringVar(),

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
                pooling = (int(values["pool"], 10), int(values["pool"], 10))
                conv.strides = stride
                conv.padding = self.widgets["combo_padding"]["widget"].get()
                conv.kernel_size = (int(values["kernel_size"] , 10), int(values["kernel_size"], 10))
                conv.filters = int(values["filters"], 10)
                
                maxpooling.pool_size = pooling
            else:
                dense = self.layers[0]
                dropout = self.layers[1]

                dense.units = int(values['neurons'])
                new_dropout = Dropout(float(values['dropout']))

                if self.is_dropout.get():
                    if dropout == None:
                        self.parent.add_dropout(dense, new_dropout)
                    else:
                        dropout.rate = float(values['dropout'])
                else:
                    if dropout != None:
                        self.parent.delete_dropout(dropout)
        else:
            Log.e(self.TAG, "Convolutional layer cannot be saved", "Invalid input")
            return
        
        Log.i(self.TAG, self.layer_type + " layer saved!")
        self.destroy()

    def delete_layer(self):
        self.grab_release()
        self.destroy()
        self.parent.delete_layer(self.layer_type, self.layers)

    def validate_values(self, values):
        if self.layer_type == CONVOLUTIONAL:
            # "filters": tk.StringVar(),
            # "stride_x": tk.StringVar(),
            # "stride_y": tk.StringVar(),

            # Pool values are 1, 2, 4, 6 and 8
            if values["pool"] == "":
                values["pool"] = "2"

            if values["kernel_size"] == "":
                values["kernel_size"] = "3"

            # Test the stride with different values of kernel size and pooling and blah blah
            if values["stride_x"] == "":
                values["stride_x"] = "1"

            if values["stride_y"] == "":
                values["stride_y"] = "1"
        return True

    def open_dropout(self):
        var = self.widgets["checkbutton_dropout"]["variable"]
        entry = self.widgets["entry_dropout"]["widget"]
    
        if var.get():
            entry.config(state='normal')
        else:
            entry.config(state='disabled')

    def render_widgets(self):
        widget_json = self.parent.parent.file_storage.widgets[self.__class__.__name__]
        self.widgets = copy.deepcopy(widget_json[WIDGETS_TYPE[self.layer_type]])
        self.save_button["pos"][0] = SAVE_BUTTON_POS[self.layer_type]
        self.widgets["save_button"] = self.save_button
        
        # Render - document
        for widget_key, value in self.widgets.items():
            pos = value.pop("pos", None)
            if "label" in widget_key:
                self.widgets[widget_key]["widget"] = tk.Label(self, cnf=self.widgets[widget_key])

            elif "checkbutton" in widget_key:
                if "command" in self.widgets[widget_key].keys() and isinstance(self.widgets[widget_key]["command"], str):
                    self.widgets[widget_key]["command"] = getattr(self, self.widgets[widget_key]["command"])

                self.widgets[widget_key]["variable"] = tk.IntVar()
                self.is_dropout = self.widgets[widget_key]["variable"]
                if self.layers[1] != None:
                    self.is_dropout.set(1)
                    self.widgets["entry_dropout"]["text"] = "self.layers[1].rate"
                
                self.widgets[widget_key]["widget"] = tk.Checkbutton(self, cnf=self.widgets[widget_key])

            elif "button" in widget_key:
                if "delete" in widget_key and not self.can_be_deleted:
                    row_number = pos[0]
                    self.save_button["pos"] = [self.save_button["pos"][0], 0, 1, 2]
                    continue

                if "command" in self.widgets[widget_key].keys() and isinstance(self.widgets[widget_key]["command"], str):
                    self.widgets[widget_key]["command"] = getattr(self, self.widgets[widget_key]["command"])
                self.widgets[widget_key]["widget"] = tk.Button(self, cnf=self.widgets[widget_key])
                
            elif "entry" in widget_key:
                widget_name = widget_key.replace("entry_", "")
                try:
                    default_value = eval(self.widgets[widget_key]["text"])
                    self.variables[widget_name].set(default_value)
                except:
                    default_value = ""

                self.widgets[widget_key]["textvariable"] = self.variables[widget_name]

                # Validate
                if "validate" in value.keys():
                    validate = value.pop("validate", None)
                    vcmd = (self.register(getattr(self, validate)))
                    widget = tk.Entry(self, validate='key', validatecommand=(vcmd, '%d', '%P', '%S'), cnf=value)
                    self.widgets[widget_key]["widget"] = widget
                else:
                    self.widgets[widget_key]["widget"] = tk.Entry(self, cnf=self.widgets[widget_key])

                # Disable dropout
                if widget_key == "entry_dropout":
                    if not self.is_dropout.get():
                        self.widgets[widget_key]["widget"].config(state='disabled')

            elif "combo" in widget_key:
                options = self.widgets[widget_key]["options"]

                try:
                    default_value = str(eval(self.widgets[widget_key]["text"]))
                    index = options.index(default_value)
                except:
                    index = 0

                var = self.variables[widget_key.replace("combo_", "")]
                var.set(default_value if default_value != None else options[index])

                widget = ttk.Combobox(self, textvariable=var, state='readonly', value=options)
                widget.current(index)
                self.widgets[widget_key]["widget"] = widget

            self.widgets[widget_key]["widget"].grid(
                row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3]
            )

    # Validate functions
    def callback_entry_pool(self, action, value_if_allowed, text):
        if action=='1':
            if text in '12468' and len(value_if_allowed) < 2:
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True
    
    def callback_entry_kernel(self, action, value_if_allowed, text):
        if action=='1':
            if text in '3579' and len(value_if_allowed) < 2:
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True
    
    def callback_entry_stride(self, action, value_if_allowed, text):
        if action=='1':
            if text in '1234' and len(value_if_allowed) < 2:
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            return False
        return True

    def callback_entry_dropout_rate(self, action, value_if_allowed, text):
        if action=='1':
            if len(value_if_allowed) == 1:
                return text == '0'
            elif len(value_if_allowed) == 2:
                return text == "."
            elif 3 <= len(value_if_allowed) <= 10:
                return text in "0123456789"

            return False
        return True
    
    def callback_entry_neurons(self, action, value_if_allowed, text):
        if action=='1':
            return text in '0123456789' and len(value_if_allowed) <= 4
        return False