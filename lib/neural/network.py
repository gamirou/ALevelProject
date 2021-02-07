import os
import json
from ..utils.log import Log
from ..neural.weights_callback import WeightsCallback
from ..utils.utils import *

# Load all libraries
import random
import copy
import tensorflow as tf
from tensorflow import keras
# import tensorflow_addons as tfa
from keras.models import Sequential
from keras.models import model_from_json, load_model
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.optimizers import SGD, Adam, RMSprop
from keras import backend as K
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np

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

    def __init__(self, network_id, directory_path, graph, session):
        # Tensorflow specific variables
        self.graph = graph
        self.session = session

        # Files
        self.network_id = network_id
        self.directory_path = directory_path

        # Model specific
        self.model = None
        self.flatten_layer = Flatten()
        self.learning_rate = 0.01
        self.optimizer = "rmsprop"
        self.is_trained = False
        self.layers = {
            "convolutional": [],
            "fully-connected": [],
            "dropout": []
        }
        #self.tqdm_callback = tfa.callbacks.TQDMProgressBar()
        self.callback = WeightsCallback()
        self.load_files()

    def new_layers(self):
        # Building the model
        self.model = Sequential()

        # Add first convolutional layer
        self.layers["convolutional"].append(Conv2D(32, (3,3), activation='relu', input_shape=(IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS)))
        
        # TODO: Change MaxPooling2D to tf.nn.max_pool2d
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Second layer
        self.layers["convolutional"].append(Conv2D(64, (3,3), activation='relu'))

        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))
        
        # Second layer
        self.layers["convolutional"].append(Conv2D(128, (3,3), activation='relu'))

        # Max pooling
        self.layers["convolutional"].append(MaxPooling2D(pool_size=(2,2)))

        # Add dropout in order to prevent overfitting
        for i in range(4):
            self.layers["dropout"].append(None)

        self.layers["dropout"][1] = Dropout(0.5)

        # Fully connected
        self.layers["fully-connected"].append(Dense(256, activation='relu'))
        
        # Output layer
        self.layers["fully-connected"].append(Dense(1, activation='sigmoid'))

    def add_layers_to_model(self):
        self.new_layers()
        for layer in self.layers["convolutional"]:
            self.model.add(layer)  

        # Flatten
        self.model.add(self.flatten_layer)

        for i in range(len(self.layers['dropout'])):
            if self.layers['dropout'][i] != None:
                self.model.add(self.layers['dropout'][i])
            
            if i < len(self.layers['fully-connected']):
                self.model.add(self.layers['fully-connected'][i])

        for layer in self.model.layers:
            Log.w(self.TAG, layer)
    
    # ORANGE HIGHLIGHT
    def are_layers_changed(self):
        network_layers = copy.copy(self.layers["convolutional"])
        network_layers.append(self.flatten_layer)
        for i in range(len(self.layers['dropout'])):
            if self.layers['dropout'][i] != None:
                network_layers.append(self.layers['dropout'][i])
            
            if i < len(self.layers['fully-connected']):
                network_layers.append(self.layers['fully-connected'][i])
        return network_layers != self.model.layers

    def reset_weights(self):
        for layer in self.model.layers: 
            if hasattr(layer, 'kernel_initializer'): 
                layer.kernel.initializer.run(session=self.session)
            if hasattr(layer, 'bias_initializer'):
                layer.bias.initializer.run(session=self.session)

    def save_weights(self):
        weights_path = os.path.join(self.directory_path, "weights")
        if not os.path.exists(weights_path):
            os.makedirs(weights_path)

        np.save(os.path.join(weights_path, f'weights_{layer.name}.npy'), weights)
        np.save(os.path.join(weights_path, f'biases_{layer.name}.npy'), biases)

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

    def get_layers_from_model(self):
        dense_index = 0
        self.layers["dropout"] = [None, None, None, None]
        for layer in self.model.layers:
            if isinstance(layer, (Conv2D, MaxPooling2D)):
                self.layers["convolutional"].append(layer)
            elif isinstance(layer, Dropout):
                self.layers["dropout"][dense_index] = layer
            elif isinstance(layer, Flatten):
                self.flatten_layer = layer
            else:
                self.layers["fully-connected"].append(layer)
                dense_index += 1

    def compile_model(self):
        # Compile the model
        # 0.2 is kinda good
        # optimiser = RMSprop(learning_rate=0.15)
        if self.optimizer == "rmsprop":
            optimizer = RMSprop(learning_rate=self.learning_rate)
        elif self.optimizer == "adam":
            optimizer = Adam(learning_rate=self.learning_rate)
        else:
            optimizer = SGD(learning_rate=self.learning_rate)

        self.model.compile(
            loss='binary_crossentropy',
            optimizer=self.optimizer,
            metrics=['accuracy'],
        )

    def predict_test_images(self, dataset, output, widget):
        with self.graph.as_default():
            K.set_session(self.session)
            pred = self.model.predict_generator(
                dataset.test_image_generator, 
                steps=dataset.test_total/dataset.batch_size, verbose=1
            )

            import time

            time.sleep(5)
            widget['text'] = 'abc'
            
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

            output.append(str(round((correct/dataset.test_total)*100, 1)) + '%')

    def predict_one_image(self, input_image, output):
        image = np.array(input_image)
        image = np.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS))
        image = image.astype('float32')
        image /= 255

        with self.graph.as_default():
            K.set_session(self.session)
            pred = self.model.predict(np.array([ image ]))
            
            output.append(pred[0][0])
            output.append("Cat" if output[0] < 0.5 else "Dog")

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

    def save_path(self, file_ending, file_name):
        self.PATHS[file_ending] = os.path.join(self.directory_path, file_name)