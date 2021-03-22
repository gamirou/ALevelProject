import os
import json
from ..neural.weights_callback import WeightsCallback
from ..utils.utils import *
import random
import copy
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, Model
from keras.models import model_from_json, load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.optimizers import SGD, Adam, RMSprop
from keras import backend as K
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np


class Network:

    PATHS = {}

    # saved here in case load_files() doesn't work
    name = ""
    description = ""
    date = ""

    def __init__(self, network_id, directory_path, graph, session):
        # Tensorflow specific variables
        self.graph = graph
        self.session = session

        # Path and neural id
        self.network_id = network_id
        self.directory_path = directory_path

        # Model specific
        self.model = None
        self.output_layer = Dense(1, activation='sigmoid')
        self.learning_rate = 0.01
        self.optimizer = "rmsprop"
        self.is_trained = False
        self.has_changed = False
        self.dropout_list_changed = False
        self.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }

        # Callback and files
        self.callback = WeightsCallback()
        self.load_files()

    """
    Default model architecture
    """
    def new_layers(self):
        # Add first convolutional layer
        self.layers["convolutional"].append(Conv2D(32, (3,3), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Second layer
        self.layers["convolutional"].append(Conv2D(64, (3,3), activation='relu'))
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))
        
        # Third layer
        self.layers["convolutional"].append(Conv2D(128, (3,3), activation='relu'))
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Dropout
        for i in range(4):
            self.layers["dropout"].append(None)

        self.layers["dropout"][1] = Dropout(0.5)

        # Dense layers
        self.layers["fully-connected"].append(Dense(256, activation='relu'))
    
    """
    Add layers to actual keras model
    """
    def add_layers_to_model(self):
        # remove all layers before adding new ones
        print(self.model)
        if self.model == None and self.has_changed == False:
            self.has_changed = True

        if self.has_changed:
            self.model = Sequential()

            layers = self.list_of_layers()
            for i, layer in enumerate(layers):
                layer._input_shape = None
                layer._output_shape = None
                self.model.add(layer)
            self.has_changed = False

    """
    Add layers from dict to a list
    """
    def list_of_layers(self):
        result = []
        for layer in self.layers["convolutional"]:
            result.append(layer)  

        # Flatten
        result.append(Flatten())

        for i in range(len(self.layers['dropout'])):
            if self.layers['dropout'][i] != None:
                result.append(self.layers['dropout'][i])
            
            if i < len(self.layers['fully-connected']):
                result.append(self.layers['fully-connected'][i])
        
        result.append(Dense(1, activation='sigmoid'))
        return result

    """
    Reset the weights of each layer
    """
    def reset_weights(self):
        for layer in self.model.layers: 
            if hasattr(layer, 'kernel_initializer'): 
                layer.kernel.initializer.run(session=self.session)
            if hasattr(layer, 'bias_initializer'):
                layer.bias.initializer.run(session=self.session)

    """
    Save weights as npy files to be loaded and read later on
    """
    def save_weights(self):
        if self.callback.weights['weights']:
            weights_path = os.path.join(self.directory_path, "weights")
            if not os.path.exists(weights_path):
                os.makedirs(weights_path)

            for layer_name, weights in self.callback.weights['weights'].items():
                np.save(os.path.join(weights_path, f'weights_{layer_name}.npy'), weights)
            for layer_name, biases in self.callback.weights['biases'].items():
                np.save(os.path.join(weights_path, f'biases_{layer_name}.npy'), biases)

    """
    Train the network
    * dataset - dataset is sent as a parameter as it is a singleton
    * epochs - the number of epochs
    """
    def train(self, dataset, epochs=None):
        with self.graph.as_default():
            K.set_session(self.session)
            self.callback.total_epochs = epochs
            fit_result = self.model.fit(
                dataset.train_image_generator,
                steps_per_epoch=int(np.ceil(dataset.train_total / float(dataset.batch_size))),
                epochs=epochs, 
                validation_data=dataset.validate_image_generator,
                validation_steps=int(np.ceil(dataset.validate_total / float(dataset.batch_size))),
                callbacks=[self.callback]
            )
            self.is_trained = True
            return fit_result

    """
    Load layers from the model in the dictionary format
    """
    def get_layers_from_model(self):
        dense_index = 0
        self.layers["dropout"] = [None, None, None, None]
        for layer in self.model.layers:
            if isinstance(layer, (Conv2D, MaxPooling2D)):
                self.layers["convolutional"].append(layer)
            elif isinstance(layer, Dropout):
                self.layers["dropout"][dense_index] = layer
            # Ignore flatten layer, we can reinitialise it when training
            # elif isinstance(layer, Flatten):
            #     self.flatten_layer = layer
            elif isinstance(layer, Dense):
                self.layers["fully-connected"].append(layer)
                dense_index += 1
        
        self.output_layer = self.layers["fully-connected"].pop()

    """
    Add the 'finishing touches' to the network
    """
    def compile_model(self):
        # Compile the model
        # 0.2 is kinda good
        # optimiser = RMSprop(learning_rate=0.15)
        if self.optimizer == "rmsprop":
            optimizer = RMSprop()
        elif self.optimizer == "adam":
            optimizer = Adam()
        else:
            optimizer = SGD(learning_rate=self.learning_rate)

        print("THIS CODE IS HERE")
        self.model.compile(
            loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=['accuracy'],
        )

    """
    Evaluate the network using the images from the test directory
    """
    def predict_test_images(self, dataset, callback_function, bridge_function, stop_progress_function):
        with self.graph.as_default():
            K.set_session(self.session)
            pred = self.model.predict_generator(
                dataset.test_image_generator,
                steps=dataset.test_total/dataset.batch_size, 
                verbose=1
            )

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
                # print(filenames[i], prediction_value)
                if (filename.split('.')[0] + 's' == prediction_value):
                    correct = correct + 1
                else:
                    incorrect = incorrect + 1

            # self.prediction_test_images = str(round((correct/dataset.test_total)*100, 1)) + '%'
            bridge_function(str(round((correct/dataset.test_total)*100, 1)) + '%', callback_function)
            stop_progress_function()

    """
    Feed in an input image to the network
    """
    def predict_one_image(self, input_image, callback_function, bridge_function, stop_progress_function):
        image = np.array(input_image)
        image = np.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS))
        image = image.astype('float32')
        image /= 255

        with self.graph.as_default():
            K.set_session(self.session)
            pred = self.model.predict(np.array([image]))
            # self.prediction_one_image = (pred[0][0], "Cat" if pred[0][0] < 0.5 else "Dog")
            bridge_function(pred[0][0], callback_function)
            stop_progress_function()

    """
    Load up model_info.txt, model_metrics.json, model.h5 and the weights numpy files
    """
    def load_files(self):
        file_names = os.listdir(self.directory_path)
        for file in file_names:
            if file.endswith("txt"):
                # Main details about user saved network
                self.save_path("txt", file)

                # Read the file
                i = 0
                attributes = []
                with open(self.PATHS["txt"], "r") as f:
                    for line in f.readlines():
                        line = line.replace("\n", "")
                        if i == 0:
                            attributes = line.split("*")
                        else:
                            values = line.split("*")
                            for j in range(len(attributes)):
                                setattr(self, attributes[j], values[j])
                        i += 1

            elif file.endswith("json"):
                # Technical details about network
                self.save_path("json", file)

                with open(self.PATHS["json"]) as json_file:
                    json_data = json.load(json_file)
                    metrics = turn_dict_values_to_float(json_data["metrics"])
                    epochs = [int(x) for x in json_data["epochs"]]
                    self.callback.set_metrics(metrics, epochs)

            elif file.endswith("h5"):
                # Actual model with weights and everything
                self.save_path("h5", file)
                self.model = load_model(self.PATHS["h5"])
            
            elif file.endswith("weights"):
                weights_dir_path = os.path.join(self.directory_path, file)
                weights = {"weights": {}, "biases":{}}
                for weights_file in os.listdir(weights_dir_path):
                    file_path = os.path.join(weights_dir_path, weights_file)
                    layer_type = type_layer_from_file(weights_file)
                    weights[layer_type[0]][layer_type[1]] = np.load(file_path)
                
                self.callback.weights = weights

    """
    Saves the path of each file based on its file type
    """
    def save_path(self, file_ending, file_name):
        self.PATHS[file_ending] = os.path.join(self.directory_path, file_name)