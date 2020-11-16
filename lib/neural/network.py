import os
import json
from ..utils.log import Log

# neural stuff
# Warnings ignore for numpy future warning (possibly tensorflow uses a different version of numpy)
import warnings
warnings.filterwarnings("ignore")

# Load all libraries
import random
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.models import model_from_json, load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Try to do digits first
from keras.datasets import mnist

# convolutional
# conv2d + maxpool2d
# dense

class Network:

    TAG = "Network"
    PATHS = {}

    # saved here in case load_files() doesn't work
    name = ""
    description = ""
    date = ""

    def __init__(self, network_id, directory_path):
        self.network_id = network_id
        self.directory_path = directory_path
        self.model = None
        self.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }
        self.load_files()

    # Stolen from Tensorflow docs
    # def pause_model(self):
    #     opt = tf.keras.optimizers.Adam(0.1)
    #     dataset = toy_dataset()
    #     iterator = iter(dataset)
    #     ckpt = tf.train.Checkpoint(step=tf.Variable(1), optimizer=opt, net=net, iterator=iterator)
    #     manager = tf.train.CheckpointManager(ckpt, './tf_ckpts', max_to_keep=3)

    def new_layers(self):
        # Building the model
        self.model = Sequential()

        # Add first convolutional layer
        # if default
        # First convolutional
        self.layers["convolutional"].append(Conv2D(32, (5,5), activation='relu', input_shape=(28, 28, 1)))
        
        # TODO: Change MaxPooling2D to tf.nn.max_pool2d
        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Second layer
        self.layers["convolutional"].append(Conv2D(32, (5,5), activation='relu'))

        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))
        
        # Flatten
        self.layers["convolutional"].append(Flatten())

        # Add dropout in order to prevent overfitting
        self.layers["dropout"].append(Dropout(0.5))
        for i in range(3):
            self.layers["dropout"].append(None)

        # Fully connected
        self.layers["fully-connected"].append(Dense(500, activation='relu'))

        # # Dropout again
        # self.layers["dropout"].append(Dropout(0.5))

        # Last 2 layers of fully connected
        self.layers["fully-connected"].append(Dense(250, activation='relu'))

        # Output layer
        self.layers["fully-connected"].append(Dense(10, activation='relu'))

    def build_model(self):
        self.new_layers()
        for layer in self.layers["convolutional"]:
            self.model.add(layer)
            
        # for layer in self.layers["fully-connected"]:
        #     self.model.add(layer)

        # for layer in self.layers["dropout"]:
        #     self.model.add(layer)    

        dense_index = 0
        for i in range(len(self.layers['dropout'])):
            if self.layers['dropout'][i] != None:
                self.model.add(self.layers['dropout'][i])
            
            if i < len(self.layers['fully-connected']):
                self.model.add(self.layers['fully-connected'][i])

    def get_layers_from_model(self):
        dense_index = 0
        self.layers["dropout"] = [None, None, None, None]
        for layer in self.model.layers:
            Log.w(self.TAG, layer)
            if isinstance(layer, (Conv2D, MaxPooling2D, Flatten)):
                self.layers["convolutional"].append(layer)
            elif isinstance(layer, Dropout):
                self.layers["dropout"][dense_index] = layer
            else:
                self.layers["fully-connected"].append(layer)
                dense_index += 1

    def compile_model(self):
        # Compile the model
        self.model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

    def load_data(self):
        (x_train, y_train), (x_test, y_test) = mnist.load_data();

        # Let's look at the shapes of the data
        print("x_train shape: ", x_train.shape)
        print("y_train shape: ", y_train.shape)
        print("x_test shape: ", x_test.shape)
        print("y_test shape: ", y_test.shape)

        # So, they are 28x28 images
        # Let's have a look at the first image
        index = random.randint(0, 1000)
        image = x_train[index]

        print("The digit is: ", y_train[index])

        plot_image = plt.imshow(image)
        plt.show()

        # print(image)

        # Normalize the data
        x_train = x_train / 255
        x_test = x_test / 255

        x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
        x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

        # Categories stored in list
        y_train_one_hot = to_categorical(y_train)
        y_test_one_hot = to_categorical(y_test)


    def load_files(self):
        file_names = os.listdir(self.directory_path)
        for file in file_names:
            if file.endswith("txt"):
                # Main details about user saved network
                self.save_path("txt", file)

                # Read the file
                i = 0;
                attributes = []
                with open(self.PATHS["txt"], "r") as f:
                    for line in f.readlines():
                        line = line.replace("\n", "")
                        if i == 0:
                            attributes = line.split(",")
                        else:
                            values = line.split(",")
                            for j in range(len(attributes)):
                                setattr(self, attributes[j], values[j])
                        i += 1

            elif file.endswith("json"):
                # Technical details about network
                self.save_path("json", file)

                with open(self.PATHS["json"]) as json_file:
                    self.json_data = json.load(json_file)

            elif file.endswith("h5"):
                # Actual model with weights and everything
                self.save_path("h5", file)
                self.model = load_model(self.PATHS["h5"])

    def save_path(self, file_ending, file_name):
        self.PATHS[file_ending] = os.path.join(self.directory_path, file_name)