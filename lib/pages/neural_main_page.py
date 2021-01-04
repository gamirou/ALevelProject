import tkinter as tk
from tkinter import ttk
from PIL import Image
from ..page import Page
from ..utils.log import Log
from ..utils.utils import *
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

    isTraining = False
    axes = {}
    widgets = {
        # will use grid system
        # "key": [label, x, y, rowspan, colspan]
    }

    inner_widgets = {
        "frame_input": {
            "label_data": {
                "text": "Data",
                "pos": [0, 0, 1, 1]
            },
            "label_description": {
                "text": "The training data needs to be 36x36 pixels",
                "wraplength": 100,
                "pos": [1, 0, 1, 1]
            },
            "label_example_image": {
                "text": "Sample image",
                "image": "image_placeholder.png", # change it self.storage['file_name']
                "pos": [2, 0, 1, 1]
            }
        },
        "frame_process": {
            "label_network": {
                "text": "Network",
                "pos": [0, 0, 1, 1]  
            },
            "button_depth": {
                "text": "Click here to see the network in more details",
                "wraplength": 100,
                "command": "go_to_edit",
                "pos": [1, 0, 1, 1]
            },
            "label_details": {
                "text": "Details",
                "pos": [2, 0, 1, 1]
            },
            # "figure_model_accuracy": {
            #     "pos": [3, 0, 1, 1]
            # }
        },
        "frame_output": {
            "label_output": {
                "text": "Output",
                "pos": [0, 0, 1, 2]  
            },
            "label_output_image": {
                "text": "Output image",
                "image": "image_placeholder.png",
                "wraplength": 100,
                "pos": [1, 0, 1, 2]
            },
            "label_result": {
                "text": "Result: ",
                "pos": [2, 0, 1, 2]
            },
            "label_accuracy": {
                "text": "Accuracy: ",
                "pos": [3, 0, 1, 2]
            },
            "button_yes": {
                "text": "YES",
                "pos": [4, 0, 1, 1]
            },
            "button_no": {
                "text": "NO",
                "pos": [4, 1, 1, 1]
            }
        }
    }

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.hist = None

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

        self.widgets["button_add_data"] = [ttk.Button(self, text="ADD TEST DATA", command=self.add_data), 2, 0, 1, 2]
        self.widgets["button_pause_train"] = [ttk.Button(self, text=TRAIN, command=self.pause_train), 2, 2, 1, 2]
        self.widgets["button_save"] = [ttk.Button(self, text="SAVE", command=self.save_network), 2, 4, 1, 2]

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
                figure = plt.Figure(figsize=(6,5), dpi=100)
                new_key = key.replace("figure_", "")
                self.axes[new_key] = figure.add_subplot(111)
                chart_type = FigureCanvasTkAgg(figure, self)
                inner_dict[key]["widget"] = chart_type.get_tk_widget()

            inner_dict[key]["widget"].grid(row=pos[0], column=pos[1], rowspan=pos[2], columnspan=pos[3])

    def fetch_network(self, network):
        # This function will run when the page is opened
        self.current_network = network
        
        # Show text and description at the top
        text = self.WELCOME_TEXT.replace("0", network.name)
        text = text.replace("1", network.description)
        self.widgets["label_name"][0]["text"] = text

        if self.current_network.model == None:
            self.current_network.build_model()
            Log.i(self.TAG, "Click the button to edit your network")
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
        if self.isTraining:
            Log.i(self.TAG, "You cannot enter the page when training data")
            return

        self.parent.update_page("NeuralEditPage")
        self.parent.pages["NeuralEditPage"].fetch_network(self.current_network)

    # Buttons
    def add_data(self):
        # self.go_to_edit()
        self.current_network.is_trained = True
        if self.current_network.is_trained:
            filename = tk.filedialog.askopenfilename()
            img = mpimg.imread(filename)
            imgplot = plt.imshow(img)
            plt.show()

            image = np.array(Image.open(filename))
            image = np.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS))
            image = image.astype('float32')
            image /= 255

            predictions = self.current_network.model.predict(np.array([ image ]))
            print(predictions)
            if predictions[0][1] > predictions[0][0]:
                Log.w(self.TAG, "It's a cat")
            else:
                Log.e(self.TAG, "It's a dog")

    def pause_train(self):
        if not self.parent.app.is_loaded:
            Log.w(self.TAG, "Loading not finished")
            return

        dataset = self.file_storage.dataset
        if self.isTraining:
            # Pause
            pass
        else:
            # Train the model
            self.current_network.compile_model()
            # x_train = dataset.data["training"] # concatenate_dataset(dataset.data["training"])
            # y_train_one_hot = dataset.categories["training"] #concatenate_dataset(dataset.categories["training"])
            
            # hist = self.current_network.model.fit(
            #     x_train, y_train_one_hot,
            #     batch_size=32,
            #     epochs=10,
            #     shuffle=True,
            #     validation_split=0.1
            # )

            fit_result = self.current_network.model.fit_generator(
                dataset.train_image_generator,
                steps_per_epoch=int(np.ceil(dataset.train_total / float(dataset.batch_size))),
                epochs=10, 
                validation_data=dataset.validate_image_generator,
                validation_steps=int(np.ceil(dataset.validate_total / float(dataset.batch_size)))
            )

            self.current_network.is_trained = True

            # self.axes["model_accuracy"].plot(hist.history['accuracy'])
            # self.axes["model_accuracy"].plot(hist.history['val_accuracy'])
            # self.axes["model_accuracy"][0].scatter(x,y, marker="o", color="r", label="Admitted")
            # self.axes["model_accuracy"][1].scatter(x,y, marker="x", color="k", label="Not-Admitted")
            # self.axes["model_accuracy"][0].set(xlabel="Exam score-1", ylabel="Exam score-2")
            # self.axes["model_accuracy"][1].set(xlabel="Exam score-1", ylabel="Exam score-2")
            # df2.plot(kind='line', legend=True, ax=self.axes["model_accuracy"], color='r',marker='o', fontsize=10)
            # self.axes["model_accuracy"].set_title('Model accuracy')

            # # Visualize model accuracy
            # plt.plot(hist.history['accuracy'])
            # plt.plot(hist.history['val_accuracy'])
            # plt.title('Model accuracy')
            # plt.xlabel('Epoch')
            # plt.ylabel('Accuracy')
            # plt.legend(['Training', 'Val'], loc='upper left')
            # plt.show()

            # # Visualize model loss
            # plt.plot(hist.history['loss'])
            # plt.plot(hist.history['val_loss'])
            # plt.title('Model loss')
            # plt.xlabel('Epoch')
            # plt.ylabel('Loss')
            # plt.legend(['Training', 'Val'], loc='upper right')
            # plt.show()

            # Test with an example
            # image_test = dataset.data["test"][random.randint(0, len(dataset["test"]))]
            # img = plt.imshow(image_test)
            # plt.title('Test image')
            # plt.show()

            # predictions = self.current_network.model.predict(np.array([ image_test ]))
            # print(predictions)

    def save_network(self):
        # code to save it
        if len(self.current_network.model.layers) == 0:
            self.current_network.add_layers_to_model()
        self.file_storage.save_network(self.current_network)
        self.current_network.layers = []
        self.parent.back_page()