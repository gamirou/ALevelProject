from PIL import Image, ImageTk
from datetime import date
import tkinter as tk
import os

ARROW_WIDTH_IMAGE = 100
ARROW_HEIGHT_IMAGE = 60
ARROW_WIDTH_CHARS = 20
ARROW_HEIGHT_CHARS = 4

CONVOLUTIONAL = "convolutional"
FULLY_CONNECTED = "fully-connected"
DROPOUT = "dropout"

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