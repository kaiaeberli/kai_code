import numpy as np
from keras.utils import np_utils
import tensorflow as tf
#tf.python.control_flow_ops = tf

# Set random seed
np.random.seed(42)

# Our data
X = np.array([[0,0],[0,1],[1,0],[1,1]]).astype('float32')
y = np.array([[0],[1],[1],[0]]).astype('float32')

# Initial Setup for Keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten

# One-hot encoding the output
y = np_utils.to_categorical(y)

# Building the model
xor = Sequential()

# each of the .add() functions is listed in the model architecture

# input and first hidden layer, specify input values, output nodes, and activation function
xor.add(Dense(8, input_shape=(2,))) # can also put function here
xor.add(Activation("relu"))

# output layer with 2 output nodes
xor.add(Dense(2))
xor.add(Activation("sigmoid")) # add sigmoid to output



xor.compile(loss="categorical_crossentropy", optimizer="adam", metrics = ['accuracy'])

# Uncomment this line to print the model architecture
xor.summary()

# Fitting the model
# Hint: This next line is where you can change the number of epochs, it's set to 10 now.
history = xor.fit(X, y, nb_epoch=100, verbose=0)

# Scoring the model
score = xor.evaluate(X, y)
print("\nAccuracy: ", score[-1])

# Checking the predictions
print("\nPredictions:")
print(xor.predict_proba(X))