import os
from PIL import Image
import numpy as np
from .utils.utils import *
from .utils.log import Log
import threading
import time

class Dataset:

    TAG = "Dataset"

    def __init__(self, file_storage, absolute_path):
        self.file_storage = file_storage
        self.path = absolute_path
        self.data = {}
        self.categories = {"training": {}, "test": {}}

        threading.Thread(target=self.load_data).start()

    def load_data(self):
        Log.i(self.TAG, "Loading started")
        self.file_storage.start_progress()
        self.create_dataset("training")
        self.create_dataset("test")
        self.file_storage.stop_progress()
        Log.i(self.TAG, "Loading stopped")
        print(time.thread_time())

    def create_dataset(self, img_type):
        img_folder = os.path.join(self.path, f"{img_type}_set")
        self.data[img_type] = {}

        limit = 1500

        for directory in os.listdir(img_folder):
            index = 0
            self.data[img_type][directory] = np.empty(shape=(limit, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS))
            for file in os.listdir(os.path.join(img_folder, directory)):
                if file.startswith("_DS"):
                    continue

                image_path = os.path.join(img_folder, directory, file)
                image = np.array(Image.open(image_path))
                image = np.resize(image, (IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS))
                image = image.astype('float32')
                image /= 255  
                self.data[img_type][directory][index] = image
                index += 1

                if index >= limit:
                    if directory == "dogs":
                        self.categories[img_type][directory] = np.array([[1, 0] for i in range(limit)])
                    else:
                        self.categories[img_type][directory] = np.array([[0, 1] for i in range(limit)])
                    break