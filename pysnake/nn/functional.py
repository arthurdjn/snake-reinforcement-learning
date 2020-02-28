# -*- coding: utf-8 -*-
# Created on Thu Feb 27 14:58:01 2020
# @author: arthurd


import numpy as np


def softmax(X):
    """
    Compute and return the softmax of the input.

    Parameters
    ----------
    X : numpy.ndarray
        Inputs of floats with shape [n, m]
        
    Returns
    -------
    numpy.ndarray
        Outputs of floats with shape [n, m]
    """

    exp = np.exp(X)
    t = X - np.log(np.sum(exp, axis=0))
    S = np.exp(t)
    return S

sigmoid = lambda X: 1.0 / (1.0 + np.exp(-X))

tanh = lambda X: np.tanh(X)

relu = lambda X: np.maximum(0, X)

leaky_relu = lambda X: np.where(X > 0, X, X * 0.01)

linear = lambda X: X