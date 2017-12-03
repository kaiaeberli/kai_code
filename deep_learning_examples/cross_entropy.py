import numpy as np


# Write a function that takes as input two lists Y, P,
# Y is a list of labels, P is the list of probabilities
# and returns the float corresponding to their cross-entropy.
def cross_entropy(Y, P):
    # get prediction for each point using model

    # get probability for each point

    # get -ln(prob) for each point, and sum them
    val = 0
    for i in range(len(P)):
        val += Y[i] * np.log(P[i]) + (1-Y[i]) * np.log(1-P[i])

    cross_entropy = -val

    return cross_entropy


# Trying for Y=[1,0,1,1] and P=[0.4,0.6,0.1,0.5].

Y = [1,0,1,1]
P = [0.4,0.6,0.1,0.5]
print(cross_entropy(Y, P))