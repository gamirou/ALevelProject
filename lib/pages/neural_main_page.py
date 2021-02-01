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
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
class NeuralMainPage(Page):

    TAG = "NeuralMainPage"

    WELCOME_TEXT = "Hello my friend! My name is 0! My description says: 1!"
    RESULT_TEXT = "Result: "
    ACCURACY_TEXT = "Accuracy: "

    is_training = False
    axes = {}    
    # "key": [label, x, y, rowspan, colspan]
    widgets = {}

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.file_storage = self.parent.file_storage
        self.inner_widgets = self.file_storage.widgets[self.__class__.__name__]
        
        # add column span to array
        self.widgets["label_name"] = [tk.Label(self, text=self.WELCOME_TEXT, bg="#00ff00"), 0, 1, 1, 4]
        # FRAMES THAT HAVE INPUT PROCESS AND OUTPUT

        self.init_inner()

        self.style = ttk.Style()
        self.style.configure("BW.TLabel", background="red")

        self.widgets["frame_input"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 0, 1, 2]
        self.widgets["frame_process"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 2, 1, 2]
        self.widgets["frame_output"] = [ttk.Frame(self, width=100, height=200, style="BW.TLabel"), 1, 4, 1, 2]

        self.widgets["button_add_data"] = [ttk.Button(self, text="ADD TEST DATA", command=self.add_data), 2, 0, 1, 2]
        self.widgets["button_train"] = [ttk.Button(self, text=TRAIN, command=self.click_train_button), 2, 2, 1, 2]
        self.widgets["button_save"] = [ttk.Button(self, text=SAVE, command=self.click_save_button), 2, 4, 1, 2]

        for key, lst in self.widgets.items():
            lst[0].grid(row=lst[1], column=lst[2], rowspan=lst[3], columnspan=lst[4])
            if "frame" in key:
                self.render_inner(key, lst)

    def render_inner(self, key, lst):
        frame = lst[0]
        inner_dict = self.inner_widgets[key]

        for key, value in inner_dict.items():
            pos = value.pop("pos", None)
            if "label" in key:
                inner_dict[key]["widget"] = tk.Label(frame, cnf=inner_dict[key])
            elif "button" in key:
                inner_dict[key]["widget"] = tk.Button(frame, cnf=inner_dict[key])
            elif "figure" in key:
                new_key = key.replace("figure_", "")
                graph_dict = {}                
                graph_dict["figure"] = plt.Figure(figsize=(6,5), dpi=100)
                graph_dict["axis"] = graph_dict["figure"].add_subplot(111)
                canvas = FigureCanvasTkAgg(graph_dict["figure"], self)
                self.parent.graphs[new_key] = graph_dict
                
                canvas.get_tk_widget().configure(cnf=inner_dict[key])
                inner_dict[key]["widget"] = canvas.get_tk_widget()

            inner_dict[key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def fetch_network(self, network):
        # This function will run when the page is opened
        self.current_network = network
        
        # DEBUG purposes
        self.current_network.is_trained = True

        # Show text and description at the top
        text = self.WELCOME_TEXT.replace("0", network.name)
        text = text.replace("1", network.description)
        self.widgets["label_name"][0]["text"] = text

        if self.current_network.model == None:
            self.current_network.add_layers_to_model()
        else:
            self.current_network.get_layers_from_model()

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
            # img = mpimg.imread(filename)
            # imgplot = plt.imshow(img)
            # plt.show()
            
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