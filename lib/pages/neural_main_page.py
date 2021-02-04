import tkinter as tk
from tkinter import ttk
from PIL import Image
from .graph_window import GraphWindow
from ..page import Page
from ..neural.network import Network
from ..frames.pop_up_confirm import PopUpConfirm
from ..utils.log import Log
from ..neural.weights_callback import WeightsCallback
from ..utils.utils import *
import threading
import random
import copy

class NeuralMainPage(Page):

    TAG = "NeuralMainPage"

    WELCOME_TEXT = "Hello my friend! My name is 0!"
    RESULT_TEXT = "Result: "
    ACCURACY_TEXT = "Accuracy: "

    is_training = False
    axes = {}    
    # "key": [label, x, y, rowspan, colspan]
    # widgets = {}
    
    frame_widgets = {
        "frame_input": {
            "side": tk.LEFT,
            "expand": True
        },
        "frame_process": {
            "side": tk.LEFT,
            "expand": True
        },
        "frame_output": {
            "side": tk.LEFT,
            "expand": True    
        },
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.file_storage = self.parent.file_storage
        self.inner_widgets = self.file_storage.widgets[self.__class__.__name__]
        self.init_inner()
        self.widgets = self.file_storage.widgets["NmpMainWidgets"]

        # Main widgets
        self.render_main_widgets()
        # self.widgets["label_name"] = [tk.Label(self, text=self.WELCOME_TEXT, bg="#00ff00"), 0, 1, 1, 4]
        # self.widgets["frame_input"] = [tk.Frame(self, width=100, height=200), 1, 0, 1, 2]
        # self.widgets["frame_process"] = [tk.Frame(self, width=100, height=200), 1, 2, 1, 2]
        # self.widgets["frame_output"] = [tk.Frame(self, width=100, height=200), 1, 4, 1, 2]

        # self.widgets["button_add_data"] = [ttk.Button(self, text="ADD TEST DATA", command=self.add_data), 2, 0, 1, 2]
        # self.widgets["button_train"] = [ttk.Button(self, text=TRAIN, command=self.click_train_button), 2, 2, 1, 2]
        # self.widgets["button_save"] = [ttk.Button(self, text=SAVE, command=self.click_save_button), 2, 4, 1, 2]

        # for key, lst in self.widgets.items():
        #     lst[0].grid(row=lst[1], column=lst[2], rowspan=lst[3], columnspan=lst[4])
        #     if "frame" in key:
        #         self.render_inner(key, lst)

    def fetch_network(self, network):
        # This function will run when the page is opened
        self.current_network = network

        # Show text and description at the top
        text = self.WELCOME_TEXT.replace("0", network.name)
        self.widgets["label_title"]["widget"]["text"] = text
        self.widgets["label_description"]["widget"]["text"] = network.description

        if self.current_network.model == None:
            self.current_network.add_layers_to_model()
        else:
            self.current_network.get_layers_from_model()

    def render_main_widgets(self, parent_widget=None, widgets=None):
        if widgets == None:
            widgets = self.widgets

        for key in widgets:
            text = widgets[key].pop("text", None)
            font = self.get_font(widgets[key])
            if "command" in widgets[key].keys():
                command = getattr(self, widgets[key].pop("command", None))
            pack_options = copy.copy(widgets[key])
            if "label" in key:
                widgets[key]["widget"] = tk.Label(self, bg="#fff", text=text, font=font, wraplength=400)
            elif "button" in key:
                widgets[key]["widget"] = ttk.Button(self, text=text, font=font, command=command)
            else:
                if key == "frame_main":    
                    widgets[key]["widget"] = tk.Frame(self, bg="#fff")
                    self.render_main_widgets(widgets[key]["widget"], self.frame_widgets)
                else:    
                    widgets[key]["widget"] = tk.Frame(parent_widget, bg="#fff")
                    self.render_inner(key, widgets[key]["widget"])

            widgets[key]["widget"].pack(pack_options)

    def render_inner(self, key, frame):
        inner_dict = self.inner_widgets[key]

        for key, value in inner_dict.items():
            pos = value.pop("pos", None)
            font = self.get_font(inner_dict[key])
            inner_dict[key]["font"] = font
            if "label" in key:
                inner_dict[key]["widget"] = tk.Label(frame, bg="#fff", cnf=inner_dict[key])
            elif "button" in key:
                inner_dict[key]["widget"] = tk.Button(frame, bg="#fff", cnf=inner_dict[key])

            inner_dict[key]["widget"].grid(
                row=pos[0], column=pos[1], rowspan=pos[2], 
                columnspan=pos[3], padx=5, pady=5
            )

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
        if self.is_training:
            Log.i(self.TAG, "You cannot enter the page when training data")
            return

        self.parent.update_page("NeuralEditPage")
        self.parent.pages["NeuralEditPage"].fetch_network(self.current_network)

    def test_network(self):
        if self.current_network.is_trained:
            # TODO: Add this function to the network class
            dataset = self.file_storage.dataset
            pred = self.current_network.model.predict_generator(dataset.test_image_generator, steps=dataset.test_total/dataset.batch_size, verbose=1)
            predicted_class_indices = np.round(pred)

            labels = (dataset.train_image_generator.class_indices)
            labels = dict((v,k) for k,v in labels.items())
            predictions = [labels[k[0]] for k in predicted_class_indices]

            filenames = dataset.test_image_generator.filenames

            correct = 0
            incorrect = 0
            for i in range(len(filenames)):
                filename = filenames[i].replace('cats_and_dogs\\', '')
                prediction_value = predictions[i]
                if (filename.split('.')[0] + 's' == prediction_value):
                    correct = correct + 1
                else:
                    incorrect = incorrect + 1

            percentage = str(round((correct/dataset.test_total)*100, 1)) + '%'
            frame_dict = self.inner_widgets["frame_output"]
            frame_dict["label_accuracy_value"]["widget"]["text"] = percentage
        else:
            Log.w(self.TAG, "Network not trained")

    # Buttons
    def add_data(self):
        # self.go_to_edit()
        if self.current_network.is_trained:
            filename = tk.filedialog.askopenfilename()
            
            image = Image.open(filename)
            self.file_storage["test_image"] = ImageTk.PhotoImage(image.resize((100, 100), Image.ANTIALIAS))
            
            frame_dict = self.inner_widgets["frame_output"]
            frame_dict["label_output_image"]["widget"].configure(image=self.file_storage["test_image"])
            frame_dict["label_output_image"]["widget"]["image"] = self.file_storage["test_image"]
            
            # Normalise it
            image = np.array(image)
            image = np.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS))
            image = image.astype('float32')
            image /= 255

            predictions = self.current_network.model.predict(np.array([ image ]))
            output = ""
            if predictions[0][0] < 0.5:
                Log.w(self.TAG, "It's a cat")
                output = "Cat"
            else:
                Log.e(self.TAG, "It's a dog")
                output = "Dog"

            frame_dict["label_result_value"]["widget"]["text"] = output
            frame_dict["label_prediction_value"]["widget"]["text"] = str(round(predictions[0][0], 5))
        else:
            Log.w(self.TAG, "Network not trained")

    def click_train_button(self):
        if not self.parent.app.is_loaded:
            Log.w(self.TAG, "Loading not finished")
            return

        if self.is_training:
            Log.w(self.TAG, "Network training in process")
            return

        message_box = PopUpConfirm(self, TRAIN, self.start_training_thread)

    def open_graph_page(self):
        self.graph_window = GraphWindow(self, self.current_network.callback)
        self.graph_window.title("Model metrics")
        self.graph_window.grab_set()

    def start_training_thread(self, epochs=None):
        self.current_network.compile_model()
        self.training_thread = threading.Thread(target=self.train_network, args=[epochs])
        self.training_thread.start()

    def delete_network_popup(self):
        message_box = PopUpConfirm(self, DELETE, self.delete_network)

    def delete_network(self):
        self.file_storage.delete_network(
            self.current_network.network_id,
            self.parent.pages["LoadingPage"]
        )
        self.parent.back_page()

    def reset_network_popup(self):
        message_box = PopUpConfirm(self, DELETE, self.reset_network)

    def reset_network(self):
        self.current_network.reset_weights()
        Log.i(self.TAG, "Network has been reset to default values")

    def train_network(self, epochs=None):
        dataset = self.file_storage.dataset
        
        # 0 to 0.5 is a cat, 0.5 to 1 is a dog
        fit_result = self.current_network.train(dataset, epochs)

        self.current_network.is_trained = True
        self.is_training = False

        # from time import sleep
        # import sys

        # epochs = 10

        # for e in range(epochs):
        #     sys.stdout.write('\r')

        #     for X, y in data.next_batch():
        #         model.fit(X, y, nb_epoch=1, batch_size=data.batch_size, verbose=0)

        #     # print loss and accuracy

        #     # the exact output you're looking for:
        #     sys.stdout.write("[%-60s] %d%%" % ('='*(60*(e+1)/10), (100*(e+1)/10)))
        #     sys.stdout.flush()
        #     sys.stdout.write(", epoch %d"% (e+1))
        #     sys.stdout.flush()

        # from keras.utils import generic_utils

        # progbar = generic_utils.Progbar(X_train.shape[0])

        # for X_batch, Y_batch in datagen.flow(X_train, Y_train):
        #     loss, acc = model_test.train([X_batch]*2, Y_batch, accuracy=True)
        #     progbar.add(X_batch.shape[0], values=[("train loss", loss), ("acc", acc)])

        # Train the model
        # x_train = dataset.data["training"] # concatenate_dataset(dataset.data["training"])
        # y_train_one_hot = dataset.categories["training"] # concatenate_dataset(dataset.categories["training"])
        
        # hist = self.current_network.model.fit(
        #     x_train, y_train_one_hot,
        #     batch_size=32,
        #     epochs=10,
        #     shuffle=True,
        #     validation_split=0.1
        # )

    def click_save_button(self):
        message_box = PopUpConfirm(self, SAVE, self.save_network)

    def save_network(self):
        # code to save it
        if len(self.current_network.model.layers) == 0:
            self.current_network.add_layers_to_model()
        self.file_storage.save_network(self.current_network)
        self.current_network.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }
        self.parent.back_page()

    def get_font(self, widget_dict):
        font_name = widget_dict.pop("font", None)
        if font_name != None:
            return self.file_storage.fonts[font_name]