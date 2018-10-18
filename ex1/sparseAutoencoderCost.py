import numpy as np
from sigmoid import sigmoid
from displayData import displayData
import scipy.stats

def sparseAutoencoderCost(theta, visibleSize, hiddenSize, _lambda, sparsityParam, beta, data):
    
    Theta1 = theta[0:hiddenSize * (visibleSize + 1)].reshape(hiddenSize, visibleSize + 1)
    Theta2 = theta[hiddenSize * (visibleSize + 1):].reshape(visibleSize, hiddenSize + 1)

    m = data.shape[0] # number of training examples

    a1 = np.vstack((np.ones(m), data.T)).T
    a2 = sigmoid(np.dot(a1, Theta1.T))

    rho = np.sum(a2, axis=0) / m
    KL = np.sum(sparsityParam*np.log(sparsityParam/rho) + (1.0-sparsityParam)*np.log((1.0-sparsityParam)/(1.0-rho)))

    a2 = np.vstack((np.ones(m), a2.T)).T
    a3 = sigmoid(np.dot(a2, Theta2.T))

    regTheta1 = Theta1[:,1:]
    regTheta2 = Theta2[:,1:]

    J = np.sum( (a3-data)*(a3-data) ) / m/2 + \
        _lambda * np.sum(regTheta1*regTheta1) / 2 + \
        _lambda * np.sum(regTheta2*regTheta2) / 2 + \
        beta * KL

    delta1 = np.zeros(Theta1.shape)
    delta2 = np.zeros(Theta2.shape)
    for i in range(m):
        a1_ = a1[i]; a2_ = a2[i]; a3_ = a3[i]
        d3 = (a3_ - data[i]) * a3_ * (1.0 - a3_)
        d2 = \
            ( \
                np.dot(d3,Theta2)[1:] + \
                beta * (-sparsityParam/rho+(1.0-sparsityParam)/(1.0-rho)) \
            ) * \
            a2_[1:] * (1.0 - a2_[1:])
        delta1 = delta1 + np.dot(d2.reshape(-1,1),a1_.reshape(1,-1))
        delta2 = delta2 + np.dot(d3.reshape(-1,1),a2_.reshape(1,-1))

    regTheta1 = np.vstack((np.zeros(Theta1.shape[0]), regTheta1.T)).T
    regTheta2 = np.vstack((np.zeros(Theta2.shape[0]), regTheta2.T)).T
    Theta1_grad = delta1 / m + _lambda * regTheta1
    Theta2_grad = delta2 / m + _lambda * regTheta2

    grad = np.append(Theta1_grad.flatten(), Theta2_grad.flatten())
    #print('cost value: %lf'%J)
    
    return J, grad
    