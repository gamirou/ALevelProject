        # from time import sleep
        # import sys

        # epochs = 10

        # for e in range(epochs):
        #     sys.stdout.write('\r')

        #     for X, y in data.next_batch():
        #         model.fit(X, y, nb_epoch=1, batch_size=data.batch_size, verbose=0)

        #     # print loss and accuracy

        #     # the exact output you're looking for:
        #     sys.stdout.write("[%-60s] %d%%" % ('='*(60*(e+1)/10), (100*(e+1)/10)))
        #     sys.stdout.flush()
        #     sys.stdout.write(", epoch %d"% (e+1))
        #     sys.stdout.flush()

        # from keras.utils import generic_utils

        # progbar = generic_utils.Progbar(X_train.shape[0])

        # for X_batch, Y_batch in datagen.flow(X_train, Y_train):
        #     loss, acc = model_test.train([X_batch]*2, Y_batch, accuracy=True)
        #     progbar.add(X_batch.shape[0], values=[("train loss", loss), ("acc", acc)])

        # Train the model
        # x_train = dataset.data["training"] # concatenate_dataset(dataset.data["training"])
        # y_train_one_hot = dataset.categories["training"] # concatenate_dataset(dataset.categories["training"])
        
        # hist = self.current_network.model.fit(
        #     x_train, y_train_one_hot,
        #     batch_size=32,
        #     epochs=10,
        #     shuffle=True,
        #     validation_split=0.1
        # )

# Neural main page
        # "key": [label, x, y, rowspan, colspan]
        # widgets = {}