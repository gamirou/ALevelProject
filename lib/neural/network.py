import os
import json
from ..utils.log import Log
from ..utils.utils import *

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
from keras.optimizers import SGD, Adam, RMSprop
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
        self.is_trained = False
        self.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }
        self.load_files()

    def new_layers(self):
        # Building the model
        self.model = Sequential()
    
        # Add first convolutional layer
        # if default
        # First convolutional
        self.layers["convolutional"].append(Conv2D(32, (3,3), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
        
        # TODO: Change MaxPooling2D to tf.nn.max_pool2d
        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Second layer
        self.layers["convolutional"].append(Conv2D(64, (3,3), activation='relu'))

        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))
        
        # Second layer
        self.layers["convolutional"].append(Conv2D(128, (3,3), activation='relu'))

        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Flatten
        self.layers["convolutional"].append(Flatten())

        # Add dropout in order to prevent overfitting
        for i in range(4):
            self.layers["dropout"].append(None)

        self.layers["dropout"][1] = Dropout(0.5)

        # Fully connected
        self.layers["fully-connected"].append(Dense(256, activation='relu'))
        
        # Output layer
        self.layers["fully-connected"].append(Dense(1, activation='sigmoid'))

    def build_model(self):
        self.new_layers()
        for layer in self.layers["convolutional"]:
            self.model.add(layer)  

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
        # 0.2 is kinda good
        # optimiser = RMSprop(learning_rate=0.15)
        self.model.compile(
            loss='binary_crossentropy',
            optimizer='rmsprop',
            metrics=['accuracy'],
        )

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