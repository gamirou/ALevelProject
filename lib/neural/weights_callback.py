from keras.callbacks import Callback
from ..utils.log import Log
import numpy as np
import os

class WeightsCallback(Callback):

    TAG = "WeightsCallback"

    # Keras callback which collects values of weights and biases at each epoch
    def __init__(self):
        super().__init__()
        self.weights = {"weights": {}, "biases": {}}
        self.epochs = []
        self.metrics = {"accuracy": [], "val_accuracy": [], "loss": [], "val_loss": []}
        self.draw_logs_function = None
        self.current_epoch = 0
        self.last_epoch = 0
        self.total_epochs = 0

    def set_draw_logs_function(self, draw_logs_function):
        self.draw_logs_function = draw_logs_function
        self.draw_logs_function(metrics=self.metrics, epochs=self.epochs)

    def set_connect_to_progress_function(self, function):
        self.update_value = function

    def set_stop_progress_function(self, function):
        self.stop_progress = function

    def set_metrics(self, metrics, epochs):
        self.metrics = metrics
        self.epochs = epochs
        self.last_epoch = len(self.epochs)

    """
    EVRIKA!!!
    THIS IS THE FUNCTION THIS IS THE FUNCTION!!!!!!
    """
    def on_train_batch_end(self, batch, logs=None):
        # Log.i(self.TAG, (batch, logs))
        self.update_value({
            'progress': int(batch*100/625),
            'logs': logs,
            'epoch': self.current_epoch + 1
        })
        
    def on_epoch_end(self, epoch, logs={}):
        self.current_epoch = epoch + 1

        self.metrics["accuracy"].append(float(logs.get('accuracy')))
        self.metrics["val_accuracy"].append(float(logs.get('val_accuracy')))
        self.metrics["loss"].append(float(logs.get('loss')))
        self.metrics["val_loss"].append(float(logs.get('val_loss')))
        self.epochs.append(epoch + self.last_epoch)

        # This will make sure we get [0, 1, 2] - a list of consecutive integers
        # When loading the json file or when finishing training, the length of the list is self.last_epoch
        if epoch == self.total_epochs - 1:
            self.last_epoch = len(self.epochs)
            self.stop_progress()
        else:
            self.update_value({
                'progress': 0,
                'logs': logs,
                'epoch': self.current_epoch
            })

        if self.draw_logs_function != None:
            self.draw_logs_function(metrics=self.metrics, epochs=self.epochs)

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
            else:
                self.weights["weights"][layer.name] = np.dstack((self.weights["weights"][layer.name], weights))
                self.weights["biases"][layer.name] = np.dstack((self.weights["biases"][layer.name], biases))