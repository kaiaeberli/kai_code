




def buildNNInLayers():
    from keras.models import Sequential
    from keras.layers.core import Dense, Activation, Flatten

    #Create the Sequential model
    model = Sequential()

    #1st Layer - Add an input layer of 32 nodes. So there are 32 inputs.
    model.add(Dense, input_dim=32)

    #2nd Layer - Add a fully connected layer of 128 nodes
    model.add(Dense(128)) # convert 32 inputs to 128 nodes.

    #3rd Layer - Add a softmax activation layer
    model.add(Activation('softmax'))

    #4th Layer - Add a fully connected layer
    model.add(Dense(10)) # there are 10 final output nodes

    #5th Layer - Add a Sigmoid activation layer
    model.add(Activation('sigmoid'))


    # compile the model, using as loss (or error) function cross entropy and performance metric accuracy
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])


    # see the model architecture
    model.summary()

    # fit model to data
    model.fit(X, y, nb_epoch=1000, verbose=0)


    # evaluate model performance using accuracy score as defined on compilation
    model.evaluate()



buildNNInLayers()