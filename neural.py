# Warnings ignore for numpy future warning (possibly tensorflow uses a different version of numpy)
import warnings
warnings.filterwarnings("ignore")

# Load all libraries
import random
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.models import model_from_json
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Try to do digits first
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data();

# Let's look at the shapes of the data
print("x_train shape: ", x_train.shape)
print("y_train shape: ", y_train.shape)
print("x_test shape: ", x_test.shape)
print("y_test shape: ", y_test.shape)

# So, they are 28x28 images
# Let's have a look at the first image
index = random.randint(0, 1000)
image = x_train[index]

print("The digit is: ", y_train[index])

plot_image = plt.imshow(image)
plt.show()

# print(image)

# Normalize the data
x_train = x_train / 255
x_test = x_test / 255

x_train = x_train.reshape(x_train.shape[0], 28, 28, 1)
x_test = x_test.reshape(x_test.shape[0], 28, 28, 1)

# Categories stored in list
y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

print(y_train)
print(y_train_one_hot)

# # Building the model
# model = Sequential()

# # Add first convolutional layer
# model.add(Conv2D(32, (5,5), activation='relu', input_shape=(28, 28, 1)))

# # TODO: Change MaxPooling2D to tf.nn.max_pool2d
# # Max pooling
# model.add(MaxPooling2D(pool_size=(2,2)))

# # Second layer
# model.add(Conv2D(32, (5,5), activation='relu'))

# # Max pooling
# model.add(MaxPooling2D(pool_size=(2,2)))

# # Flatten
# model.add(Flatten())

# # Add dropout in order to prevent overfitting
# model.add(Dropout(0.5))

# # Fully connected
# model.add(Dense(500, activation='relu'))

# # Dropout again
# model.add(Dropout(0.5))

# # Last 2 layers of fully connected
# model.add(Dense(250, activation='relu'))

# # Output layer
# model.add(Dense(10, activation='relu'))

# # Compile the model
# model.compile(
#     loss='categorical_crossentropy',
#     optimizer='adam',
#     metrics=['accuracy']
# )

# # Our brain is ready to be trained
# hist = model.fit(
#     x_train, y_train_one_hot,
#     batch_size=256,
#     epochs=10,
#     validation_split=0.2
# )

# # Evaluate the model
# model.evaluate(
#     x_test, y_test_one_hot
# )

# # Visualize model accuracy
# plt.plot(hist.history['accuracy'])
# plt.plot(hist.history['val_accuracy'])
# plt.title('Model accuracy')
# plt.xlabel('Epoch')
# plt.ylabel('Accuracy')
# plt.legend(['Training', 'Val'], loc='upper left')
# plt.show()

# # Visualize model loss
# plt.plot(hist.history['loss'])
# plt.plot(hist.history['val_loss'])
# plt.title('Model loss')
# plt.xlabel('Epoch')
# plt.ylabel('Loss')
# plt.legend(['Training', 'Val'], loc='upper right')
# plt.show()

# # Test with an example
# image_test = x_test[random.randint(1000, 2002)]
# img = plt.imshow(image_test)
# plt.title('Test image')
# plt.show()

# predictions = model.predict(np.array([ image_test ]))
# list_index = [i for i in range(0, 10)]
# x = predictions

# for i in range(10):
#     for j in range(10):
#         if x[0][list_index[i]] > x[0][list_index[j]]:
#             temp = list_index[i]
#             list_index[i] = list_index[j]
#             list_index[j] = temp


# for i in range(10):
#     print("{}. Digit {}".format(i+1, list_index[i]))


# model_json = model.to_json()
# with open("neural/model.json", "w") as json_file:
#     json_file.write(model_json)
# # serialize weights to HDF5
# model.save_weights("neural/model.h5")
# model.save("neural/model_easy.h5")
# print("Saved model to disk")