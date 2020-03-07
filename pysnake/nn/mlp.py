# -*- coding: utf-8 -*-
# Created on Thu Feb 27 14:57:53 2020
# @author: arthurd


import numpy as np
from pysnake.nn.functional import softmax, relu


class NeuralNetwork(object):
    """
    Multi Layer Perceptron.
    """
    
    def __init__(self, layer_dimensions, params = None, activation_function = relu):
        self.layer_dimensions = layer_dimensions
        self.params = params if params is not None else self._init_params(layer_dimensions)
        self.activation_function = activation_function
    
        
    # -------------------------------------------------------------------------
    # Methods
    
    def _init_params(self, layer_dimensions):
        """
        Initialize the parameters of the network.

        Parameters
        ----------
        layer_dimensions : list(int)
            A list of length L+1 with the number of nodes in each layer, 
            including the input layer, all hidden layers, and the output layer.

        Returns
        -------
        dict
            A dictionary with initialized parameters for all parameters 
            (weights and biases) in the network.
        """
        
        # Creating the parameters dict
        params = {}    
        # Depth of the neural network
        depth = len(layer_dimensions)
        # Create the weights and biases
        for i in range(1, depth):
            mu = 0
            var = 2 / layer_dimensions[i]
            sigma = np.sqrt(var)
            # Weights
            W_shape = (layer_dimensions[i - 1], layer_dimensions[i])
            W = np.random.normal(loc=mu, scale=sigma, size=W_shape)
            b = np.zeros((layer_dimensions[i], 1))
            # Saving in the param dict
            layer_W = "W_" + str(i)
            params[layer_W] = W
            layer_b = "b_" + str(i)
            params[layer_b] = b
        return params
             
    
    def forward(self, X_batch):
        """One forward step.
    
        Args:
            X_batch: float numpy array with shape [n^[0], batch_size].
            params: python dict with weight and bias parameters for each layer.
    
        Returns:
            Y_proposed: float numpy array with shape [n^[L], batch_size]. The output predictions of the
                        network, where n^[L] is the number of prediction classes. For each input i in
                        the batch, Y_proposed[c, i] gives the probability that input i belongs to class
                        c.
        """       
        # Get the layers dimension
        layer_dimensions = self.layer_dimensions
        depth = len(layer_dimensions) - 1
        # 1/ Iterates through the depth of the neural network
        Z = X_batch   
        self.params['A_0'] = Z
        for i in range(1, depth + 1):
            # 1.1/ Get the weights and biases from the params       
            layer_W = "W_" + str(i)
            layer_b = "b_" + str(i)
            W = self.params[layer_W]
            b = self.params[layer_b]
                            
            # 1.2/ Compute the outputs
            Z = np.dot(W.T, Z) + b
            
            # 2/ Activation
            # The activation only occurs in the hidden layers,
            # not from the last hidden layer to the outputs
            if i < depth:
                Z = self.activation_function(Z)
                self.params['A_' + str(i)] = Z
            
        # 3/ Softmax
        Y_proposed = softmax(Z)
        self.params['A_' + str(i)] = Y_proposed
    
        return Y_proposed
    