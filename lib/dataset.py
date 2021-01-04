import os
from PIL import Image, ImageChops
import numpy as np
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from .utils.utils import *
from .utils.log import Log
import threading
import time
import random

class Dataset:

    TAG = "Dataset"

    def __init__(self, file_storage, absolute_path):
        self.file_storage = file_storage
        self.path = absolute_path
        self.data = {}
        self.categories = {"training": {}, "test": {}}
        self.thread_running = True

        # DEBUG Option
        # self.load_data()
        threading.Thread(target=self.load_data).start()
        # thread.setDaemon(True)
        # thread.start()

    def load_data(self):
        Log.i(self.TAG, "Loading started")
        # self.create_dataset("training")
        # self.create_dataset("test")
        self.datagen()
        self.file_storage.is_loading = False
        Log.i(self.TAG, "Loading stopped")
        print(time.thread_time())

    def datagen(self):
        self.batch_size = 32

        # Directories as os objects
        train_dir = os.path.join(self.path, 'train')
        validate_dir = os.path.join(self.path, 'validation')
        test_dir = os.path.join(self.path, 'test')
        train_dogs_dir = os.path.join(train_dir, 'dogs')
        train_cats_dir = os.path.join(train_dir, 'cats')
        validate_dogs_dir = os.path.join(validate_dir, 'dogs')
        validate_cats_dir = os.path.join(validate_dir, 'cats')
        test_cats_and_dogs_dir = os.path.join(test_dir, 'cats_and_dogs')

        num_dogs_train = len(os.listdir(train_dogs_dir))
        num_cats_train = len(os.listdir(train_cats_dir))
        num_dogs_validate = len(os.listdir(validate_dogs_dir))
        num_cats_validate = len(os.listdir(validate_cats_dir))

        self.train_total = num_dogs_train + num_cats_train
        self.validate_total = num_dogs_validate + num_cats_validate
        self.test_total = len(os.listdir(test_cats_and_dogs_dir))

        # Initialise generators
        self.image_generator = ImageDataGenerator(rescale=1./255)
        self.train_image_generator = self.image_generator.flow_from_directory(
            batch_size=self.batch_size,
            directory=train_dir,
            shuffle=True,
            target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
            class_mode='binary'
        )

        self.validate_image_generator = self.image_generator.flow_from_directory(
            batch_size=self.batch_size,
            directory=validate_dir,
            shuffle=False,
            target_size=(IMAGE_WIDTH, IMAGE_HEIGHT),
            class_mode='binary'
        )

        self.test_image_generator = self.image_generator.flow_from_directory(
            batch_size=self.batch_size,
            directory=test_dir,
            shuffle=False,
            target_size=(IMAGE_WIDTH, IMAGE_WIDTH),
            class_mode=None
        )

    def create_dataset(self, img_type):
        # limit = 100 # 3900 
        is_np_available = 'normalised' in os.listdir(self.path)
        if is_np_available:
            is_np_available = f"{img_type}_set" in os.listdir(os.path.join(self.path, 'normalised'))

        if not is_np_available:
            img_folder = os.path.join(self.path, f"{img_type}_set")
            directories = os.listdir(img_folder)
            limit = len(os.listdir(os.path.join(img_folder, directories[0]))) - 1
            
            num_augmented = 6
            arr_length = limit * 2 * num_augmented
            indexes_available = [i for i in range(arr_length)]

            self.data[img_type] = np.empty(shape=(arr_length, IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS))
            self.categories[img_type] = np.empty(shape=(arr_length, 2))

            i = 0
            for directory in directories:
                for file in os.listdir(os.path.join(img_folder, directory)):
                    if file.startswith("_DS"):
                        continue

                    # Read data and normalise it
                    image_path = os.path.join(img_folder, directory, file)
                    images = self.augmented_images(Image.open(image_path))
                    indexes = []
                    for image in images:
                        image = np.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS))
                        image = image.astype('float32')
                        image /= 255 

                        # Get index
                        index = random.choice(indexes_available)
                        indexes_available.remove(index)

                        # We need to shuffle the data
                        # Numpy array with the indexes shuffled from 0 to limit * 2

                        self.data[img_type][index] = image
                        if directory == "dogs":
                            self.categories[img_type][index] = np.array([1, 0])
                        else:
                            self.categories[img_type][index] = np.array([0, 1])
                    
                    # image = np.array(Image.open(image_path))
                    # image = np.resize(image, (IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS))
                    # image = image.astype('float32')
                    # image /= 255 
                        
                    i += 1
                    if i % limit == 0:
                        print(i, limit)
                        try:
                            os.makedirs(f"{self.path}\\normalised\\{img_type}_set")
                        except FileExistsError:
                            pass
                        folder_path = os.path.join(self.path, 'normalised', f"{img_type}_set")
                        np.save(os.path.join(folder_path, "data.npy"), self.data[img_type])
                        np.save(os.path.join(folder_path, "categories.npy"), self.categories[img_type])

                        break
        else:
            folder_path = os.path.join(self.path, 'normalised', f"{img_type}_set")
            self.data[img_type] = np.load(os.path.join(folder_path, "data.npy"))
            self.categories[img_type] = np.load(os.path.join(folder_path, "categories.npy"))

    def augmented_images(self, image):
        augmented = []
        original_np = np.array(image)
        augmented.append(original_np)

        # 1. horizontal flipping
        augmented.append(np.fliplr(original_np))

        # 2. rotation using matrix
        augmented.append(np.array(image.rotate(-45)))
        augmented.append(np.array(image.rotate(45)))

        # 3. shifting
        augmented.append(np.array(ImageChops.offset(image, random.randint(-10, 10), 0)))
        augmented.append(np.array(ImageChops.offset(image, 0, random.randint(-10, 10))))
        
        return augmented
        
    # TODO: Develop your own shifting algorithm
    # def shifting(self, arr, dy, dx):
    #     if dy != 0:
    #         pass

    #     def operation(offset):
    #         return
