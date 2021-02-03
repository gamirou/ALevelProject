from keras.callbacks import Callback
from ..utils.log import Log
import numpy as np

class WeightsCallback(Callback):
    # Keras callback which collects values of weights and biases at each epoch
    def __init__(self):
        super().__init__()
        self.weights = {"weights": {}, "biases": {}}
        self.logs = []
        self.epochs = []
        self.metrics = {"accuracy": [], "val_accuracy": []}
        self.bridge_function = None
        self.last_epoch = 0
        self.total_epochs = 0

    def set_bridge_function(self, bridge_function):
        self.bridge_function = bridge_function
        self.bridge_function(metrics=self.metrics, epochs=self.epochs)

    def set_metrics(self, metrics, epochs):
        self.metrics = metrics
        self.epochs = epochs
        self.last_epoch = len(self.epochs)

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.metrics["accuracy"].append(float(logs.get('accuracy')))
        self.metrics["val_accuracy"].append(float(logs.get('val_accuracy')))
        self.metrics["loss"].append(float(logs.get('loss')))
        self.metrics["val_loss"].append(float(logs.get('val_loss')))
        self.epochs.append(epoch + self.last_epoch)
        
        # This will make sure we get [0, 1, 2] - a list of consecutive integers
        # When loading the json file or when finishing training, the length of the list is self.last_epoch
        if epoch == self.total_epochs - 1:
            self.last_epoch = len(self.epochs)

        if self.bridge_function != None:
            self.bridge_function(metrics=self.metrics, epochs=self.epochs)

        for layer in self.model.layers:
            try:
                weights = layer.get_weights()[0]
                biases = layer.get_weights()[1]

            # Talk about this index error and how different layers store weights
            except IndexError:
                continue
            
            if epoch == 0:
                self.weights["weights"][layer.name] = weights
                self.weights["biases"][layer.name] = biases

                # np.save(f'weights_{layer.name}.npy', weights)
                # np.save(f'biases_{layer.name}.npy', biases)
            else:
                self.weights["weights"][layer.name] = np.dstack((self.weights["weights"][layer.name], weights))
                self.weights["biases"][layer.name] = np.dstack((self.weights["biases"][layer.name], biases))