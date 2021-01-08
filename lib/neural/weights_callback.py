from keras.callbacks import Callback
from ..utils.log import Log
import numpy as np
import warnings
warnings.filterwarnings("ignore")

class WeightsCallback(Callback):
    # Keras callback which collects values of weights and biases at each epoch
    def __init__(self):
        super().__init__()
        self.weights = {"weights": {}, "biases": {}}
        self.logs = []
        self.metrics = {"accuracy": [], "val_accuracy": []}
        self.epochs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        print(self.logs)
        self.metrics["accuracy"].append(logs.get('accuracy'))
        self.metrics["val_accuracy"].append(logs.get('val_accuracy'))
        self.epochs.append(epoch)

        for layer in self.model.layers:
            try:
                weights = layer.get_weights()[0]
                biases = layer.get_weights()[1]

            except IndexError:
                continue
            
            if epoch == 0:
                self.weights["weights"][layer.name] = weights
                self.weights["biases"][layer.name] = biases
            else:
                self.weights["weights"][layer.name] = np.dstack((self.weights["weights"][layer.name], weights))
                self.weights["biases"][layer.name] = np.dstack((self.weights["biases"][layer.name], biases))