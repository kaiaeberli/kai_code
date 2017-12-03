import numpy as np


# Write a function that takes as input a list of numbers, and returns
# the list of values given by the softmax function.
def softmax(L):
    # first do softmax function as e^(z_i) / (sum(e^(Z))
    sumE = np.sum(np.exp(L))
    res = []
    for elem in L:
        res.append(np.exp(elem) / sumE)

    return res


softmax([1,2,3,4])