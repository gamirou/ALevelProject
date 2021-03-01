import tkinter as tk
from tkinter import ttk
import copy
import threading
from ..utils.utils import *
from ..frames.tooltip import ToolTip
import matplotlib.pyplot as plt
from keras.layers import Dropout
from keras.models import Model
from keras import backend as K
from keras.preprocessing.image import load_img, img_to_array
from math import sqrt

class LayerWindow(tk.Toplevel):

    def __init__(
        self, master=None, layer_type=None, layers=(), can_be_deleted=True, 
        weights=(), inputs=None, cnf={}, **kw
    ):
        super().__init__(master=master, bg="#fff", cnf=cnf, **kw)
        self.parent = master
        self.tooltip = ToolTip()
        self.can_be_deleted = can_be_deleted
        self.weights = weights
        self.inputs = inputs
        self.model = None
        
        # Functions that depend on the window
        self.bind('<Configure>', self.configure_tooltip)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

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
        self.update_empty_values(values)
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

        self.parent.parent.notify(self.layer_type.capitalize() + " layer saved!")
        self.destroy()

    def delete_layer(self):
        if tk.messagebox.askokcancel("Delete layer", "Are you sure? It will be gone forever if you click 'OK'"):
            self.grab_release()
            self.destroy()
            self.parent.delete_layer(self.layer_type, self.layers)

    def update_empty_values(self, values):
        if self.layer_type == CONVOLUTIONAL:
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

    def open_dropout(self):
        var = self.widgets["checkbutton_dropout"]["variable"]
        entry = self.widgets["entry_dropout"]["widget"]
    
        if var.get():
            entry.config(state='normal')
        else:
            entry.config(state='disabled')

    def render_widgets(self):
        widget_json = self.parent.file_storage.widgets[self.__class__.__name__]
        self.widgets = copy.deepcopy(widget_json[WIDGETS_TYPE[self.layer_type]])
        self.save_button["pos"][0] = SAVE_BUTTON_POS[self.layer_type]
        self.widgets["save_button"] = self.save_button
        
        # Render - document
        for widget_key, value in self.widgets.items():
            pos = value.pop("pos", None)
            info_term = value.pop("info", None)

            if info_term:
                parent_frame = tk.Frame(self, bg="#fff")
            else:
                parent_frame = self

            if "label" in widget_key:
                self.widgets[widget_key]["widget"] = tk.Label(parent_frame, bg="#fff", cnf=self.widgets[widget_key])

            elif "checkbutton" in widget_key:
                if "command" in self.widgets[widget_key].keys() and isinstance(self.widgets[widget_key]["command"], str):
                    self.widgets[widget_key]["command"] = getattr(self, self.widgets[widget_key]["command"])

                self.widgets[widget_key]["variable"] = tk.IntVar()
                self.is_dropout = self.widgets[widget_key]["variable"]
                if self.layers[1] != None:
                    self.is_dropout.set(1)
                    self.widgets["entry_dropout"]["text"] = "self.layers[1].rate"
                
                self.widgets[widget_key]["widget"] = tk.Checkbutton(parent_frame, bg="#fff", cnf=self.widgets[widget_key])

            elif "button" in widget_key:
                if "delete" in widget_key and not self.can_be_deleted:
                    row_number = pos[0]
                    self.save_button["pos"] = [self.save_button["pos"][0], 0, 1, 2]
                    continue

                # boolean algebra
                weights_buttons = ("button_view_biases", "button_view_weights", "button_view_filters", "button_view_feature_maps")
                if widget_key in weights_buttons and len(self.weights) == 0:
                    continue

                if "command" in self.widgets[widget_key].keys() and isinstance(self.widgets[widget_key]["command"], str):
                    self.widgets[widget_key]["command"] = getattr(self, self.widgets[widget_key]["command"])
                
                self.widgets[widget_key]["widget"] = tk.Button(parent_frame, bg="#fff", cnf=self.widgets[widget_key])
                
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
                    widget = tk.Entry(parent_frame, bg="#fff", validate='key', validatecommand=(vcmd, '%d', '%P', '%S'), cnf=value)
                    self.widgets[widget_key]["widget"] = widget
                else:
                    self.widgets[widget_key]["widget"] = tk.Entry(parent_frame, bg="#fff", cnf=self.widgets[widget_key])

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

                widget = ttk.Combobox(parent_frame, textvariable=var, state='readonly', value=options)
                widget.current(index)
                self.widgets[widget_key]["widget"] = widget

            # Add info button
            if info_term:
                parent_frame.grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])
                definition = self.parent.file_storage.get_definition_by_term(info_term)
                info_button = tk.Button(
                    parent_frame, bg='#fff', width=32, height=32, relief='flat',
                    image=self.parent.file_storage['info_button_icon.png']
                )
                self.widgets[widget_key]["widget"].pack(side=tk.LEFT)
                info_button.pack(side=tk.LEFT)
                self.tooltip.add_widget(info_button, definition)
            else:
                self.widgets[widget_key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def view_filters(self):
        # viewer = WeightsViewer(self, self.weights[0], state=FILTERS)
        filters = np.copy(self.weights[0])
        f_min, f_max = filters.min(), filters.max()
        filters = (filters - f_min) / (f_max - f_min)

        n_filters, ix = 6, 1
        for i in range(n_filters):
            # get the filter
            f = filters[:, :, :, i]
            # plot each channel separately
            for j in range(3):
                # specify subplot and turn of axis
                ax = plt.subplot(n_filters, 3, ix)
                # ax.set_xticks([])
                # ax.set_yticks([])
                # plot filter channel in grayscale
                # grayscale allows you to visualise it better, but filters look really cool in colour
                plt.imshow(f[:, :, j], cmap='gray')
                ix += 1
        # show the figure
        plt.show(block=False)

    def view_feature_maps(self):
        # viewer = WeightsViewer(self, self.weights[0], state=FEATURE_MAPS)
        if self.model == None:
            self.model = Model(inputs=self.inputs, outputs=self.layers[0].output)
        
        filename = tk.filedialog.askopenfilename()
        if filename != "":
            img = load_img(filename, target_size=IMAGE_SIZE)
            # convert the image to an array
            img = img_to_array(img)
            # expand dimensions so that it represents a single 'sample'
            img = np.expand_dims(img, axis=0)
            # prepare the image (e.g. scale pixel values for the vgg)
            img /= 255.0
            self.feature_map_thread = threading.Thread(
                target=self.thread_generate_feature_maps, 
                args=[
                    # mainview = self.parent.parent (first parent is neural edit page)
                    img, self.parent.parent.pages['NeuralMainPage'].send_thread_output_to_app, 
                    self.plot_feature_maps
                ]
            )
            self.feature_map_thread.start()
    
    def plot_feature_maps(self, feature_maps):
        # plot the output from each block
        width = 8
        # only include 64 feature maps, it gets too slow at 128 and 256
        height = int((self.layers[0].filters if self.layers[0].filters <= 64 else 64) / width)
        for fmap in feature_maps:
            # plot all 64 maps in an 8x8 squares
            ix = 1
            for i in range(width):
                for j in range(height):
                    # specify subplot and turn of axis
                    # fig.canvas.set_window_title('Test')
                    ax = plt.subplot(width, height, ix)
                    ax.set_xticks([])
                    ax.set_yticks([])
                    # plot filter channel in grayscale
                    
                    plt.imshow(fmap[:, :, ix-1], cmap='gray')
                    ix += 1
            # show the figure
            plt.show(block=False)

    def thread_generate_feature_maps(self, img, bridge_function, callback_function):
        with self.parent.file_storage.graph.as_default():
            K.set_session(self.parent.file_storage.session)
            feature_maps = self.model.predict(img)
            bridge_function(feature_maps, callback_function)

    def configure_tooltip(self, event=None):
        if self.tooltip.top_level != None:
            x = y = 0
            x, y, cx, cy = self.tooltip.active_widget.bbox("insert")
            x += self.tooltip.active_widget.winfo_rootx() + self.tooltip.offset['x']
            y += self.tooltip.active_widget.winfo_rooty() + self.tooltip.offset['y']
            self.tooltip.top_level.geometry(f"+{x}+{y}")

    def close_window(self):
        if tk.messagebox.askokcancel("Close layer", "Are you sure? Your progress will not be saved"):
            self.destroy()

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