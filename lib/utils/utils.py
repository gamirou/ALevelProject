from PIL import Image, ImageTk
from datetime import date
import numpy as np
import tkinter as tk
import os

ARROW_WIDTH_IMAGE = 100
ARROW_HEIGHT_IMAGE = 60
ARROW_WIDTH_CHARS = 20
ARROW_HEIGHT_CHARS = 4

CONVOLUTIONAL = "convolutional"
FULLY_CONNECTED = "fully-connected"
DROPOUT = "dropout"

# Type of widget
WIDGETS_TYPE = {
    CONVOLUTIONAL: "conv_widgets",
    FULLY_CONNECTED: "fully_connected_widgets"
}

SAVE_BUTTON_POS = {
    CONVOLUTIONAL: 8,
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

# Messages
POPUP_MESSAGES = {
    SAVE: "Are you sure you want to save the network?",
    TRAIN: "Are you sure you want to train the network?",
    BUILD_MODEL: "Are you sure you want to overwrite the previous model?",
    DELETE: "Are you sure you want to delete this network? This action cannot be undone!",
    RESET_ARCHITECTURE: "Are you sure you want to reset your model to default? Your changes will be lost!"
}

IMAGE_WIDTH = 52
IMAGE_HEIGHT = 52
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