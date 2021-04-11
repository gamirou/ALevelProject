from keras.callbacks import Callback
import numpy as np
import os

class WeightsCallback(Callback):

    """
    Keras callback which collects values of weights and biases at each epoch
    """
    
    def __init__(self):
        super().__init__()
        self.weights = {"weights": {}, "biases": {}}
        self.epochs = []
        self.metrics = {"accuracy": [], "val_accuracy": [], "loss": [], "val_loss": []}
        self.draw_logs_function = None
        self.current_epoch = 1
        self.last_epoch = 0
        self.total_epochs = 0

    """
    Store a reference to the draw_logs function inside GraphWindow in order to call it
    """
    def set_draw_logs_function(self, draw_logs_function):
        self.draw_logs_function = draw_logs_function
        self.draw_logs_function(metrics=self.metrics, epochs=self.epochs)

    """
    'Bridge' function that sends the logs to the progress bar
    """
    def set_connect_to_progress_function(self, function):
        self.update_value = function

    """
    'Bridge' function that stops the progress bar once network has been trained
    """
    def set_stop_progress_function(self, function):
        self.stop_progress = function

    """
    Sets metrics from loaded JSON file
    """
    def set_metrics(self, metrics, epochs):
        self.metrics = metrics
        self.epochs = epochs
        self.last_epoch = len(self.epochs)

    """
    EVRIKA!!!
    THIS IS THE FUNCTION THIS IS THE FUNCTION!!!!!!
    This function is self-explanatory
    """
    def on_train_batch_end(self, batch, logs=None):
        self.update_value({
            'progress': int(batch*100/625),
            'logs': logs,
            'epoch': self.current_epoch
        })
    
    """
    Again, self-explanatory function
    """
    def on_epoch_end(self, epoch, logs={}):
        self.current_epoch = epoch + 2

        # Get the logs
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
            self.current_epoch = 1
        else:
            # Reset the progress bar
            self.update_value({
                'progress': 0,
                'logs': logs,
                'epoch': self.current_epoch
            })

        # Draw the logs on the graphs
        if self.draw_logs_function != None:
            self.draw_logs_function(metrics=self.metrics, epochs=self.epochs)

        # Store the weights inside a dictionary of numpy arrays
        for layer in self.model.layers:
            try:
                weights = layer.get_weights()[0]
                biases = layer.get_weights()[1]

            # Talk about this index error and how different layers store weights
            except IndexError:
                continue
            
            # TODO: This is sus
            # Add to numpy array or create new array
            # if epoch == 0:
            self.weights["weights"][layer.name] = weights
            self.weights["biases"][layer.name] = biases
            # else:
            #     self.weights["weights"][layer.name] = np.dstack((self.weights["weights"][layer.name], weights))
            #     self.weights["biases"][layer.name] = np.dstack((self.weights["biases"][layer.name], biases))