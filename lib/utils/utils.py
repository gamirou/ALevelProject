from PIL import Image, ImageTk
from datetime import date
import numpy as np
import tkinter as tk
import os
import re

# Initial size
APP_SIZE = 700
MAX_LAYERS = 4

# Back page button
ARROW_WIDTH_IMAGE = 100
ARROW_HEIGHT_IMAGE = 60
ARROW_WIDTH_CHARS = 20
ARROW_HEIGHT_CHARS = 4
INITIAL_SCROLLED_TEXT_WIDTH = 10

# Types of layers
CONVOLUTIONAL = "convolutional"
FULLY_CONNECTED = "fully-connected"
DROPOUT = "dropout"

# Type of widget
WIDGETS_TYPE = {
    CONVOLUTIONAL: "conv_widgets",
    FULLY_CONNECTED: "fully_connected_widgets"
}

SAVE_BUTTON_POS = {
    CONVOLUTIONAL: 9,
    FULLY_CONNECTED: 4
}

# States of pop up boxes
RESET_MODEL = "RESET MODEL"
TRAIN = "TRAIN"
PAUSE = "PAUSE"
SAVE = "SAVE"
BUILD_MODEL = "BUILD MODEL"
DELETE = "DELETE"
RESET_ARCHITECTURE = "RESET ARCHITECTURE"
CLOSE_WINDOW = "CLOSE WINDOW"

# Progress bar states
DETERMINATE = 'determinate'
INDETERMINATE = 'indeterminate'

# Weights viewer states
WEIGHTS = 'weights'
BIASES = 'biases'
FILTERS = 'filters'
FEATURE_MAPS = 'feature maps'

# Messages
POPUP_MESSAGES = {
    SAVE: "Are you sure you want to save the network?",
    TRAIN: "Are you sure you want to train the network?",
    BUILD_MODEL: "Are you sure you want to reset the weights? This action cannot be undone and you will have to train the network again!",
    DELETE: "Are you sure you want to delete this network? This action cannot be undone!",
    RESET_ARCHITECTURE: "Are you sure you want to reset your model to default? Your changes will be lost!",
    CLOSE_WINDOW: "Are you sure? Your progress on this network will not be saved, do you want to save the network first?"
}

# Image
IMAGE_WIDTH = 128
IMAGE_HEIGHT = 128
IMAGE_SIZE = (IMAGE_WIDTH, IMAGE_HEIGHT)
IMAGE_CHANNELS = 3

def resize_image(image, size):
    img = image.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(img)

def today():
    return str(date.today())

def create_file(folder, file_name, file_content):
    file_path = get_main_path(folder, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(file_content)

def get_main_path(folder, file_name):
    script_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) #<-- absolute dir the script is in
    rel_path = "{}\\{}".format(folder, file_name)
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path

def get_image_from_folder(file_name):
    file_path = get_main_path("images", file_name)
    image = Image.open(file_path)
    return ImageTk.PhotoImage(image)

def turn_to_camel_case(string):
    return ''.join(x for x in string.title() if x != "_")

def turn_dict_values_to_float(dictionary):
    for key, value in dictionary.items():
        try:
            new_value = float(value)
        except TypeError:
            new_value = [float(x) for x in value]
        
        dictionary[key] = new_value

    return dictionary

def get_os_name():
    import platform
    return platform.system()

def type_layer_from_file(file_name):
    file_name = file_name.replace('.npy', '')
    weights_type = "biases" if file_name.startswith('b') else "weights"
    layer_name = file_name.replace(weights_type + "_", "")
    return (weights_type, layer_name)

def find_all_occurences(original_string, substring):
    return [ch.start() for ch in re.finditer(substring, original_string)]