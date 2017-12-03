import numpy as np
# Setting the random seed, feel free to change it and see different solutions.
np.random.seed(42)

def sigmoid(x):
    return 1/(1+np.exp(-x))
def sigmoid_prime(x):
    return sigmoid(x)*(1-sigmoid(x))

#prediction with sigmoid
def prediction(X, W, b):
    return sigmoid(np.matmul(X,W)+b)

# cross entropy function
def error_vector(y, y_hat):
    return [-y[i]*np.log(y_hat[i]) - (1-y[i])*np.log(1-y_hat[i]) for i in range(len(y))]

# error function
def error(y, y_hat):
    ev = error_vector(y, y_hat)
    return sum(ev)/len(ev)

# TODO: Fill in the code below to calculate the gradient of the error function.
# The result should be a list of three lists:
# The first list should contain the gradient (partial derivatives) with respect to w1
# The second list should contain the gradient (partial derivatives) with respect to w2
# The third list should contain the gradient (partial derivatives) with respect to b
def dErrors(X, y, y_hat):

    # this does all the partial derivs at the same time
    # so each points partial deriv wrt x1, wrt x2 and wrt b
    DErrorsDx1 = (y - y_hat[:,0]) * (X[:,0])
    DErrorsDx2 = (y-y_hat[:,0]) * X[:,1]
    DErrorsDb = (y-y_hat[:,0])

    """
    seems to be some issue with the quiz - above gives an error
    DErrorsDx1 = [X[i][0] * (y[i] - y_hat[i]) for i in range(len(y))]
    DErrorsDx2 = [X[i][1] * (y[i] - y_hat[i]) for i in range(len(y))]
    DErrorsDb = [y[i] - y_hat[i] for i in range(len(y))]
    """

    return DErrorsDx1, DErrorsDx2, DErrorsDb

# TODO: Fill in the code below to implement the gradient descent step.
# The function should receive as inputs the data X, the labels y,
# the weights W (as an array), and the bias b.
# It should calculate the prediction, the gradients, and use them to
# update the weights and bias W, b. Then return W and b.
# The error e will be calculated and returned for you, for plotting purposes.
def gradientDescentStep(X, y, W, b, learn_rate = 0.01):

    # this does the prediction for all points at the same time
    # TODO: Calculate the prediction
    y_hat = prediction(X, W, b)

    # gets partial derivs for each point
    # TODO: Calculate the gradient
    grad = dErrors(X, y, y_hat)

    # update weights for equation, must be sequentially after using each points
    #  partial derivs
    # TODO: Update the weights
    # actually, could also update weights with sum * learning_rate

    # see: weights are changed even for correctly classified points.
    for iPoint in range(len(y)):
        W[0] += learn_rate * grad[0][iPoint]
        W[1] += learn_rate * grad[1][iPoint]
        b += learn_rate * grad[2][iPoint]

    # This calculates the error
    e = error(y, y_hat)
    return W, b, e

# This function runs the perceptron algorithm repeatedly on the dataset,
# and returns a few of the boundary lines obtained in the iterations,
# for plotting purposes.
# Feel free to play with the learning rate and the num_epochs,
# and see your results plotted below.
def trainLR(X, y, learn_rate = 0.01, num_epochs = 100):
    x_min, x_max = min(X.T[0]), max(X.T[0])
    y_min, y_max = min(X.T[1]), max(X.T[1])
    # Initialize the weights randomly
    W = np.array(np.random.rand(2,1))*2 -1
    b = np.random.rand(1)[0]*2 - 1
    # These are the solution lines that get plotted below.
    boundary_lines = []
    errors = []
    for i in range(num_epochs):
        # In each epoch, we apply the gradient descent step.
        W, b, error = gradientDescentStep(X, y, W, b, learn_rate)
        boundary_lines.append((-W[0]/W[1], -b/W[1]))
        errors.append(error)
    return boundary_lines, errors



import numpy as np
raw_data = open("data.csv", 'rt')
data = np.loadtxt(raw_data, delimiter=",")
X = data[:,[0,1]]
y = data[:,2]

print(trainLR(X, y)[1])